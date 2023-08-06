import os
import subprocess
class langrun:

    def python_interactive():
        subprocess.call(['python', '-i'])

    def python(filename, *args):
        subprocess.call(['python', filename] + list(args))

    @staticmethod
    def c(filename):
        os.system(f"gcc {filename} -o {filename}.out")
        os.system(f"./{filename}.out")
        
    @staticmethod
    def cpp(filename):
        os.system(f"g++ {filename} -o {filename}.out")
        os.system(f"./{filename}.out")
        
    @staticmethod
    def csharp(filename):
        os.system(f"mcs {filename}.cs")
        os.system(f"mono {filename}.exe")
        
    @staticmethod
    def java(filename):
        os.system(f"javac {filename}.java")
        os.system(f"java {filename}")

    @staticmethod
    def ruby(filename):
        os.system(f"ruby {filename}")
        
    @staticmethod
    def javascript(filename):
        os.system(f"node {filename}")
        
    @staticmethod
    def php(filename):
        os.system(f"php {filename}")
        
    @staticmethod
    def perl(filename):
        os.system(f"perl {filename}")
        
    @staticmethod
    def bash(filename):
        os.system(f"bash {filename}")
        
    @staticmethod
    def go(filename):
        os.system(f"go run {filename}")
        
    @staticmethod
    def kotlin(filename):
        os.system(f"kotlinc {filename}.kt -include-runtime -d {filename}.jar")
        os.system(f"java -jar {filename}.jar")
        
    @staticmethod
    def rust(filename):
        os.system(f"rustc {filename}.rs")
        os.system(f"./{filename}")
        
    @staticmethod
    def swift(filename):
        os.system(f"swift {filename}")
        
    @staticmethod
    def julia(filename):
        os.system(f"julia {filename}")
        
    @staticmethod
    def lua(filename):
        os.system(f"lua {filename}")
        
    @staticmethod
    def groovy(filename):
        os.system(f"groovy {filename}")
        
    @staticmethod
    def dart(filename):
        os.system(f"dart {filename}")
        
    @staticmethod
    def r(filename):
        os.system(f"Rscript {filename}")
        
    @staticmethod
    def erlang(filename):
        os.system(f"escript {filename}")
        
    @staticmethod
    def haskell(filename):
        os.system(f"runghc {filename}")
        
    @staticmethod
    def scala(filename):
        os.system(f"scala {filename}")