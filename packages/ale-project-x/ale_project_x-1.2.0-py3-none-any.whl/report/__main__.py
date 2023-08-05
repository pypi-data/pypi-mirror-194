from report import worker, INPUT_FOLDER, OUTPUT_FOLDER
import sys, argparse, os

def main():
    print("Running main")
    print("Run below command: gen --input 'input_path' --output 'output_path'")
    parser = argparse.ArgumentParser(
                    prog = 'ProgramName',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
    parser.add_argument("command")
    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    print(args)
    
    if (args.command == 'gen'):
        print('gen report')
        input_folder_path = args.input
        
        print(input_folder_path)
        output_folder_path = args.output
        if not os.path.isdir(output_folder_path): 
            create_folder = input("Folder doesn't exist, create folder? (Y/N)")
            if create_folder.upper() == "Y":
                os.mkdir(output_folder_path)
            else:
                return
        print(output_folder_path)
        worker.run(INPUT_FOLDER, output_folder_path)
        return
    else:
        print('Invalid command')
        return
    
if __name__ == "__main__":
    main()