import os
import pprint
import datetime
import time
from .files import path_is_in_path, generate_file_list, determine_file_extension
from .handlers import HandlerManager
from .time import human_delta
from .modes import Mode

# from multiprocessing import Pool, cpu_count
from pathos.multiprocessing import ProcessingPool as Pool

import logging

logger = logging.getLogger(__name__)

now = datetime.datetime.now()

gzip_suffix = ".gz"


class Processor:
    def __init__(self, settings: dict):
        self.settings = settings
        self.input = settings.get("input", None)
        self.output = settings.get("output", None)
        self.input_is_dir = self.input and os.path.isdir(self.input)
        self.input_exists = self.input and os.path.exists(self.input)
        self.output_is_dir = self.output and os.path.isdir(self.output)
        self.output_exists = self.output and os.path.exists(self.output)

        self.mode: Mode = Mode(settings.get("mode", "minify"))
        self.format: bool = settings.get("format", False)
        self.overwrite: bool = settings.get("overwrite", False)
        self.on_change: bool = settings.get("on_change", False)
        self.prefix: bool = settings.get("prefix", False)
        self.gzip: bool = settings.get("gzip", False)
        self.hash: bool = settings.get("hash", False)
        self.verbose: bool = settings.get("verbose", False)
        self.force: bool = settings.get("force", False)
        self.dry_run: bool = settings.get("dry_run", False)
        self.nproc: int = settings.get("nproc", 1)

        self.handlers = HandlerManager()
        self.handlers.prepare_handlers(self.settings)

        self.valid_extensions = self.handlers.get_supported_extensions()
        self.handler_names = self.handlers.get_handler_names()

        if self.verbose:
            logger.info("### Settings:")
            logger.info(pprint.pformat(self.settings))
            logger.info("### Handlers:")
            logger.info(pprint.pformat(self.handler_names))
            logger.info("### Valid extensions:")
            logger.info(pprint.pformat(self.valid_extensions))
        self.pool = None

    def sanity_checks(self):
        valid_modes = list(Mode)
        if not self.mode in valid_modes:
            return (False, f"The specified mode {self.mode} was not valid. NOTE: Valid modes are {pprint.pformat(valid_modes)}")
        if not self.input or not self.input_exists:
            return (False, f"The input specified '{self.input}' did not exist. Input must be an existing directory or file")
        if not self.overwrite and self.on_change:
            return (False, f"On-change will not have an effect so long as overwrite is not enabled")
        if not self.output and not self.overwrite and not self.format:
            return (False, f"Only input '{self.input}' was specified. Without a setting for 'output', 'overwrite' and/or 'format' all processing will fail")
        if path_is_in_path(self.input, self.output):
            return (False, f"The output '{self.output}' is a subpath of input '{self.input}'")
        if path_is_in_path(self.output, self.input):
            return (False, f"The input '{self.input}' is a subpath of output '{self.output}'")
        return True, None

    def process_file(self, input_path: str, output_path: str):
        if self.verbose:
            logger.info(f"Processing '{input_path}' to '{output_path}'")
        if not input_path:
            return False, False, False, ["No input path specified"]
        if not output_path:
            return False, False, False, ["No output path specified"]
        input_mtime = os.path.getmtime(input_path)
        output_mtime = None
        if os.path.isfile(output_path):
            if not self.overwrite:
                return False, False, False, ["Trying to overwrite without overwrite enabled"]
            if self.on_change:
                output_mtime = os.path.getmtime(output_path)
                if not self.overwrite and not self.force and (input_mtime == output_mtime):
                    return True, False, True, ["File not changed, skipping"]
                elif not self.overwrite and not self.force and (output_mtime > input_mtime):
                    return True, False, True, [f"Destination file newer than input, skipping ({output_mtime} >= {input_mtime})"]
        else:
            output_dir = os.path.dirname(output_path)
            if not os.path.isdir(output_dir):
                os.makedirs(name=output_dir, exist_ok=True)
            if not os.path.isdir(output_dir):
                return False, False, False, ["Output directory did not exist or could not be created"]
        extension, raw_extension = determine_file_extension(input_path)
        vip_file = False
        if not extension:
            # Skip well known files with unsupported file extensions
            base_name = os.path.basename(input_path)
            if base_name in ["sitemap.xml", "favicon.ico", "robots.txt"]:
                vip_file = True
            else:
                return False, False, False, [f"Unknown extension '{raw_extension}' for input file"]
        handler = None
        is_binary = True
        if not vip_file:
            handler = self.handlers.get_handler_by_extension(extension)
            if not handler:
                return False, False, False, [f"Could not find handler for input file with extension {extension}"]
            is_binary = handler.is_binary()
        original_content = None
        try:
            with open(input_path, "rb") if is_binary else open(input_path, "r", encoding="utf-8") as file:
                original_content = file.read()
        except Exception as err:
            return False, False, False, [f"Could not load data from input file: {err}"]
        if not original_content:
            logger.warning(f"Input file '{input_path}' was empty")
        processed_content = None
        handler_errors = None
        was_copied = False
        do_copy = handler is None or vip_file or (handler.name() in self.handler_names and self.settings.get(f"disable_type_{handler.name()}", False)) or (extension in self.valid_extensions and self.settings.get(f"disable_suffix_{extension}", False))
        if do_copy:
            # Perform copy
            # logger.info(f"SUPPOSED TO COPY: {input_path} ({extension})")
            processed_content = original_content
            was_copied = True
        else:
            # logger.info(f"SUPPOSED TO PROCESS: {input_path} ({extension})")
            _processed_content, handler_errors = handler.process(original_content, input_path)
            processed_content = _processed_content
        # logger.info(f"Content of file {input_path} was of type {type(original_content)} while processed {type(processed_content)}")
        if handler_errors:
            return False, False, False, handler_errors
        if None == processed_content:
            logger.warning(f"Processed file '{input_path}' was empty")
        try:
            if not self.dry_run:
                with open(output_path, "wb") if is_binary else open(output_path, "w", encoding="utf-8") as file:
                    written = file.write(processed_content)
                    if written != len(processed_content):
                        return False, False, False, [f"Partially written output ({written} of {len(processed_content)} bytes)"]
        except Exception as err:
            return False, False, False, [f"Could not write data to output file: {err}"]
        try:
            if not self.dry_run:
                os.utime(output_path, (input_mtime, input_mtime))
        except Exception as err:
            return False, False, False, [f"Could not modify date of output file: {err}"]
        if self.gzip:
            try:
                gzip_path = f"{output_path}{gzip_suffix}"
                if not self.dry_run:
                    with open(gzip_path, "wb") as gzip_file:
                        gzip_content = zlib.compress(processed_content, level=9)
                        gzip_written = gzip_file.write(gzip_content)
                        if gzip_written != len(gzip_content):
                            return False, False, False, [f"Partially written gzip output ({gzip_written} of {len(gzip_content)} bytes)"]
            except Exception as err:
                return False, False, False, [f"Could not write gzip data to output file: {err}"]
            try:
                if not self.dry_run:
                    os.utime(gzip_content, (input_mtime, input_mtime))
            except Exception as err:
                return False, False, False, [f"Could not modify date of gzip file: {err}"]
        # All went well, go home happy!
        return True, was_copied, False, []

    def process_files_list_item_wrapper(self, item):
        input_path = item["input_path"]
        output_path = item["output_path"]
        single_start_time = datetime.datetime.now()
        result = {}
        # success, copied, skipped, message = self.process_file(input_path=input_path, output_path=output_path)
        result["success"], result["copied"], result["skipped"], result["messages"] = self.process_file(input_path=input_path, output_path=output_path)
        result["input_path"] = input_path
        result["output_path"] = output_path
        result["single_start_time"] = single_start_time
        single_end_time = datetime.datetime.now()
        single_interval = single_end_time - single_start_time
        result["single_end_time"] = single_end_time
        result["single_interval"] = single_interval
        result["was_slow"] = single_interval > datetime.timedelta(seconds=1)
        if result.get("was_slow"):
            result["messages"].extend([f"Processing of {result.get('input_path')} was slow ({human_delta(result.get('single_interval'))})"])
        return result

    def process_files_list(self, list):
        start_time = datetime.datetime.now()
        success_count = 0
        copied_count = 0
        skipped_count = 0
        messages = {}
        results = []
        if self.dry_run:
            logger.info(f"Dry run enabled, changes will NOT be commited to filesystem")
        if self.nproc > 1:
            logger.info(f"Doing multiprocessing with {self.nproc} cores")
            with Pool(self.nproc) as pool:
                results = pool.map(self.process_files_list_item_wrapper, list)
        else:
            logger.info(f"Doing sequential processing")
            for item in list:
                result = self.process_files_list_item_wrapper(item)
                results.append(result)
        # Summarize results
        for result in results:
            if result.get("success"):
                success_count += 1
            if result.get("copied"):
                copied_count += 1
            if result.get("skipped"):
                skipped_count += 1
            input_path = f"{result.get('input_path')}"
            for message in result.get("messages"):
                all = messages.get(message, [])
                messages[message] = [*all, input_path]
        end_time = datetime.datetime.now()
        interval = end_time - start_time
        failed = len(list) - success_count
        logger.info(f"Processing of {len(list)} files with {success_count} successful, {copied_count} copied and {skipped_count} skipped, generated {len(messages)} message(s) and took {human_delta(interval)} total")
        if messages:
            logger.warning(f"Messages encountered were:")
            for message, all in messages.items():
                logger.warning(f"{len(all)} x {message}")
                show_count = 5
                count = len(all)
                for index in range(min(show_count, count)):
                    logger.warning(f"    {all[index]}")
                if show_count < count:
                    logger.warning(f"    ... and {count-show_count} more")
                logger.warning("")
        return True

    def _process_existing_dir_to_existing_dir(self):
        input_paths = generate_file_list(self.input, tuple(self.valid_extensions))
        # logger.info(pprint.pformat(input_paths))
        list = []
        for input_path in input_paths:
            common = os.path.commonpath((os.path.abspath(self.output), os.path.abspath(input_path)))
            rel = os.path.relpath(os.path.abspath(input_path), os.path.abspath(self.input))
            output_path = os.path.join(os.path.abspath(self.output), rel)
            list.append({"input_path": input_path, "output_path": output_path})
        # logger.info(pprint.pformat(list))
        return list

    def _process_existing_dir_to_new_dir(self):
        # This is same as _process_existing_dir_to_existing_dir but with a mkdir first
        os.mkdir(self.output)
        self.output_exists = self.output and os.path.exists(self.output)
        return self._process_existing_dir_to_existing_dir()

    def _process_existing_dir_overwrite(self):
        input_paths = generate_file_list(self.input, tuple(self.valid_extensions))
        # logger.info(pprint.pformat(input_paths))
        list = []
        for input_path in input_paths:
            list.append({"input_path": input_path, "output_path": input_path})
        # logger.info(pprint.pformat(list))
        return list

    def process_files(self):
        not_implemented = "not implemented"
        if self.input_is_dir:
            if self.output:
                if self.output_is_dir:
                    if self.verbose:
                        logger.info(f"existing-dir-to-existing-dir easy peasy case")
                    list = self._process_existing_dir_to_existing_dir()
                    return self.process_files_list(list), None
                elif not self.output_exists:
                    if self.verbose or True:
                        logger.info(f"existing-dir-to-new-dir easy peasy case")
                    list = self._process_existing_dir_to_new_dir()
                    return self.process_files_list(list), None
                else:
                    return None, f"existing-dir-to-existing-file error"
            elif self.overwrite:
                if self.verbose or True:
                    logger.info(f"existing-dir-overwrite easy peasy case")
                list = self._process_existing_dir_overwrite()
                return self.process_files_list(list), None
            elif self.format:
                return None, f"format: {not_implemented}"
            else:
                return None, f"input dir specified without valid output option"
        else:
            if self.output:
                if self.output_is_dir:
                    return None, f"existing-file-to-existing-dir easy peasy case: {not_implemented}"
                elif not self.output_exists:
                    return None, f"existing-file-to-new-file easy peasy case: {not_implemented}"
                else:
                    if self.overwrite:
                        return None, f"existing-file-to-existing-file overwrite easy peasy case: {not_implemented}"
                    else:
                        return None, f"existing-file-to-existing-file non-overwrite error"
            elif self.overwrite:
                return None, "overwrite: {not_implemented} 2"
            elif self.format:
                return None, "format: {not_implemented} 2"
            else:
                return None, f"input file specified without valid output option 2"
