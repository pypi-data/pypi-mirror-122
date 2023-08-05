import os
import glob
import csv
import pkg_resources
from scyllaso.util import find_java, log_important, log


class HdrLogProcessor:

    def __init__(self, properties, warmup_seconds=None, cooldown_seconds=None):
        self.properties = properties
        self.java_path = find_java(self.properties)
        self.warmup_seconds = warmup_seconds
        self.cooldown_seconds = cooldown_seconds
        module_dir = os.path.dirname(pkg_resources.resource_filename('scyllaso', '__init__.py'))
        self.lib_dir = os.path.join(module_dir, "lib")
        print("lib_dir:"+str(self.lib_dir))

    def __trim(self, file):
        filename = os.path.basename(file)
        filename_no_ext = os.path.splitext(filename)[0]

        old_cwd = os.getcwd()
        new_cwd = os.path.dirname(os.path.realpath(file))
        os.chdir(new_cwd)

        args = f'union -if {filename} -of trimmed_{filename_no_ext}.hdr'
        if self.warmup_seconds is not None:
            args = f'{args} -start {self.warmup_seconds}'
        if self.cooldown_seconds is not None:
            args = f'{args} -end {self.cooldown_seconds}'

        cmd = f'{self.java_path} -cp {self.lib_dir}/processor.jar CommandDispatcherMain {args}'
        log(cmd)
        os.system(cmd)
        os.chdir(old_cwd)

    def trim_recursivly(self, dir):
        if self.warmup_seconds is None and self.warmup_seconds is None:
            return

        log_important("HdrLogProcessor.trim_recursively")

        for hdr_file in glob.iglob(dir + '/*/*.hdr', recursive=True):
            filename = os.path.basename(hdr_file)
            if filename.startswith("trimmed_"):
                continue

            log(hdr_file)
            self.__trim(hdr_file)

        log_important("HdrLogProcessor.trim_recursively")

    def merge_recursivly(self, dir):
        log_important("HdrLogProcessor.merge_recursively")
        log(dir)
        # todo be careful with merging the merge file.
        files_map = {}

        for hdr_file in glob.iglob(dir + '/*/*.hdr', recursive=True):
            log(hdr_file)
            base = os.path.splitext(os.path.basename(hdr_file))[0]
            files = files_map.get(base)
            if files is None:
                files = []
                files_map[base] = files
            files.append(hdr_file)

        for name, files in files_map.items():
            input = ""
            for file in files:
                input = input + " -ifp " + file
            cmd = f'{self.java_path} -cp {self.lib_dir}/processor.jar CommandDispatcherMain union {input} -of {dir}/{name}.hdr'
            log(cmd)
            os.system(cmd)

        log_important("HdrLogProcessor.merge_recursively")

    def __summarize(self, file):
        filename = os.path.basename(file)
        filename_no_ext = os.path.splitext(filename)[0]
        old_cwd = os.getcwd()
        new_cwd = os.path.dirname(os.path.realpath(file))
        os.chdir(new_cwd)

        summary_text_name = f"{filename_no_ext}-summary.txt"
        summary_csv_name = f"{filename_no_ext}-summary.csv"

        args = f'-if {filename_no_ext}.hdr'
        os.system(
            f'{self.java_path} -cp {self.lib_dir}/processor.jar CommandDispatcherMain summarize {args} >  {summary_text_name}')

        entries = {}
        with open(summary_text_name, 'r') as summary_text_file:
            for line in summary_text_file:
                row = line.split('=')
                entries[row[0].strip()] = row[1].strip()

        with open(summary_csv_name, 'w') as summary_csv_file:
            header = ','.join(entries.keys())
            content = ','.join(entries.values())
            summary_csv_file.write(f'{header}\n')
            summary_csv_file.write(f'{content}\n')

        os.chdir(old_cwd)

    def summarize_recursivly(self, dir):
        log_important("HdrLogProcessor.summarize_recursively")
        for hdr_file in glob.iglob(dir + '/**/*.hdr', recursive=True):
            log(hdr_file)
            self.__summarize(hdr_file)
        log_important("HdrLogProcessor.summarize_recursively")

    def __process(self, file):
        filename = os.path.basename(file)
        filename_no_ext = os.path.splitext(filename)[0]
        old_cwd = os.getcwd()
        new_cwd = os.path.dirname(os.path.realpath(file))
        os.chdir(new_cwd)

        tags = set()
        with open(filename, "r") as hdr_file:
            reader = csv.reader(hdr_file, delimiter=',')
            # Skip headers
            for i in range(5):
                next(reader, None)
            for row in reader:
                first_column = row[0]
                tag = first_column[4:]
                tags.add(tag)

        for tag in tags:
            # process twice; once to get the csv formatted output and again for the non csv output.
            logprocessor = f'{self.java_path} -cp {self.lib_dir}/HdrHistogram-2.1.9.jar org.HdrHistogram.HistogramLogProcessor'
            args = f'-i {filename} -o {filename_no_ext + "_" + tag} -tag {tag} -csv'
            os.system(f'{logprocessor} {args}')
            os.rename(f'{filename_no_ext + "_" + tag}.hgrm', f'{filename_no_ext + "_" + tag}.hgrm.csv')

            args = f'-i {filename} -o {filename_no_ext + "_" + tag} -tag {tag}'
            os.system(f'{logprocessor} {args}')

        os.chdir(old_cwd)

    def process_recursivly(self, dir):
        log_important("HdrLogProcessor.summarize_recursively")
        for hdr_file in glob.iglob(dir + '/**/*.hdr', recursive=True):
            log(hdr_file)
            self.__process(hdr_file)
        log_important("HdrLogProcessor.summarize_recursively")
