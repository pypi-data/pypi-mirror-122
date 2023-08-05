class Progressbar:
    def __init__(self, total, length, prefix, suffix, decimals, output_progress):
        self.total = total
        self.length = length
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.output_progress = output_progress

    def print_progress(self, iteration, action=None):
        progress_bar = self.__build_progress_bar(iteration)
        if action is not None and self.output_progress:
            print(' ' * len(progress_bar), end='\r')
            print(action)
        print(progress_bar, end='\r')
        if iteration == self.total: 
            print(progress_bar)

    def __build_progress_bar(self, iteration):
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (iteration / float(self.total)))
        filled_length = int(self.length * iteration // self.total)
        bar = '█' * filled_length + '-' * (self.length - filled_length)
        return f'{self.prefix} |{bar}| {percent}% {self.suffix}'