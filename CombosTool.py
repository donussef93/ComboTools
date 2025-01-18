import os
import random
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.progress import Progress
from rich.panel import Panel
from rich import print
from tkinter import Tk, filedialog
from datetime import datetime
console = Console()

banner = '''

▄• ▄▌▄▄▌  ▄▄▄▄▄▪  • ▌ ▄ ·.  ▄▄▄· ▄▄▄▄▄▄▄▄ .     ▄▄·       • ▌ ▄ ·. ▄▄▄▄·
█▪██▌██•  •██  ██ ·██ ▐███▪▐█ ▀█ •██  ▀▄.▀·    ▐█ ▌▪▪     ·██ ▐███▪▐█ ▀█▪▪
█▌▐█▌██▪   ▐█.▪▐█·▐█ ▌▐▌▐█·▄█▀▀█  ▐█.▪▐▀▀▪▄    ██ ▄▄ ▄█▀▄ ▐█ ▌▐▌▐█·▐█▀▀█▄ ▄█▀▄
▐█▄█▌▐█▌▐▌ ▐█▌·▐█▌██ ██▌▐█▌▐█ ▪▐▌ ▐█▌·▐█▄▄▌    ▐███▌▐█▌.▐▌██ ██▌▐█▌██▄▪▐█▐█▌.▐▌
 ▀▀▀ .▀▀▀  ▀▀▀ ▀▀▀▀▀  █▪▀▀▀ ▀  ▀  ▀▀▀  ▀▀▀     ·▀▀▀  ▀█▄▀▪▀▀  █▪▀▀▀·▀▀▀▀  ▀█▄▀▪


          [+++++] : Improved by @donussef
          
          [1] Combine Multiple Files                                                                                  │
│         [2] Split File by Lines or Size                                                                             │
│         [3] Randomize Lines                                                                                         │
│         [4] Sort Lines Alphabetically                                                                               │
│         [5] Extract Lines with Keyword                                                                              │
│         [6] Remove Duplicate Lines                                                                                  │
│         [7] Filter Lines by Domain                                                                                  │
│         [8] Convert URL✉password to email:password                                                                  │
│         [9] Convert email:password to user:password                                                                 │
│         [10] Remove Lines Matching Keyword                                                                          │
│         [11] Search and Replace                                                                                     │
│         [12] Check for Invalid Lines                                                                                │
│          Quit                                                                                                       │
│
'''

def file_dialog_multiple():
    """Open a file dialog to select multiple files."""
    Tk().withdraw()
    files = filedialog.askopenfilenames(title='Select Text Files', filetypes=[('Text Files', '*.txt')])
    return files

def file_dialog_single():
    """Open a file dialog to select a single file."""
    Tk().withdraw()
    file = filedialog.askopenfilename(title='Select Text File', filetypes=[('Text Files', '*.txt')])
    return file

def get_output_file_path(function_name, folder_name):
    """Create a folder named by function ran and return an output file path with a timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_dir = os.path.join(os.getcwd(), folder_name)
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, f'{function_name}_{timestamp}.txt')

def preview_output(lines):
    """Show the first 10 lines of the output before saving."""
    console.print('\n[cyan]Preview (First 10 lines):[/cyan]')
    for line in lines[:10]:
        console.print(line.strip())
    console.print('\n[green]Preview complete.[/green]')

def convert_url_to_email_password():
    file = file_dialog_single()
    if not file:
        console.print('[red]No file selected![/red]')
        return
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    converted_lines = []
    for line in lines:
        parts = line.strip().split(':')
        if len(parts) >= 4:
            email_password = f'{parts[1]}:{parts[2]:{parts[3]}}\n'
            converted_lines.append(email_password)
    output_file = get_output_file_path('url_to_email_password', 'url_to_email_password_files')
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.writelines(converted_lines)
    preview_output(converted_lines)
    console.print(f'[green]URLs converted to email:password and saved to {output_file}[/green]')

def convert_email_to_user_password():
    file = file_dialog_single()
    if not file:
        console.print('[red]No file selected![/red]')
        return
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    converted_lines = []
    for line in lines:
        if ':' in line and '@' in line.split(':')[0]:
            email, password = line.strip().split(':')
            user = email.split('@')[0]
            converted_lines.append(f'{user}:{password}\n')
    output_file = get_output_file_path('email_to_user_password', 'email_to_user_password_files')
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.writelines(converted_lines)
    preview_output(converted_lines)
    console.print(f'[green]Emails converted to user:password and saved to {output_file}[/green]')

def remove_lines_with_keyword():
    file = file_dialog_single()
    if not file:
        console.print('[red]No file selected![/red]')
        return
    keyword = Prompt.ask('Enter the keyword to remove lines containing it')
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    remaining_lines = [line for line in lines if keyword not in line]
    output_file = get_output_file_path('lines_without_keyword', 'lines_without_keyword_files')
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.writelines(remaining_lines)
    preview_output(remaining_lines)
    console.print(f"[green]Lines without the keyword '{keyword}' saved to {output_file}[/green]")

def combine_files():
    files = file_dialog_multiple()
    if not files:
        console.print('[red]No files selected![/red]')
        return
    combined_content = ''
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            combined_content += f.read() + '\n'
    output_file = get_output_file_path('combined', 'combined_files')
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write(combined_content)
    preview_output(combined_content.splitlines())
    console.print(f'[green]Files combined and saved to {output_file}[/green]')

def split_file_by_line_or_size():
    file = file_dialog_single()
    if not file:
        console.print('[red]No file selected![/red]')
        return
    choice = Prompt.ask('Split by [L]ines or [S]ize?', choices=['L', 'S'])
    folder_name = 'split_files'
    os.makedirs(folder_name, exist_ok=True)
    if choice == 'L':
        lines_per_file = int(Prompt.ask('How many lines per file?'))
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for i in range(0, len(lines), lines_per_file):
            output_file = get_output_file_path(f'split_{i // lines_per_file + 1}', folder_name)
            with open(output_file, 'w', encoding='utf-8') as split_file:
                split_file.writelines(lines[i:i + lines_per_file])
            console.print(f'[green]Created {output_file}[/green]')
    else:
        file_size = int(Prompt.ask('Enter the maximum file size (in KB)?')) * 1024
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        current_size = 0
        current_file_lines = []
        file_counter = 1
        for line in lines:
            current_size += len(line.encode('utf-8'))
            current_file_lines.append(line)
            if current_size >= file_size:
                output_file = get_output_file_path(f'split_{file_counter}', folder_name)
                with open(output_file, 'w', encoding='utf-8') as split_file:
                    split_file.writelines(current_file_lines)
                console.print(f'[green]Created {output_file}[/green]')
                file_counter += 1
                current_file_lines = []
                current_size = 0
        if current_file_lines:
            output_file = get_output_file_path(f'split_{file_counter}', folder_name)
            with open(output_file, 'w', encoding='utf-8') as split_file:
                split_file.writelines(current_file_lines)
            console.print(f'[green]Created {output_file}[/green]')

def randomize_lines():
    file = file_dialog_single()
    if not file:
        console.print('[red]No file selected![/red]')
        return
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    random.shuffle(lines)
    output_file = get_output_file_path('randomized', 'randomized_files')
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.writelines(lines)
    preview_output(lines)
    console.print(f'[green]Lines randomized and saved to {output_file}[/green]')

def sort_lines():
    file = file_dialog_single()
    if not file:
        console.print('[red]No file selected![/red]')
        return
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines.sort()
    output_file = get_output_file_path('sorted', 'sorted_files')
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.writelines(lines)
    preview_output(lines)
    console.print(f'[green]Lines sorted and saved to {output_file}[/green]')

def extract_lines_with_keyword():
    file = file_dialog_single()
    if not file:
        console.print('[red]No file selected![/red]')
        return
    keyword = Prompt.ask('Enter the keyword to search for')
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    matched_lines = [line for line in lines if keyword in line]
    output_file = get_output_file_path('extracted', 'extracted_files')
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.writelines(matched_lines)
    preview_output(matched_lines)
    console.print(f"[green]Lines containing the keyword '{keyword}' saved to {output_file}[/green]")

def remove_duplicate_lines():
    file = file_dialog_single()
    if not file:
        console.print('[red]No file selected![/red]')
        return
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    unique_lines = list(set(lines))
    output_file = get_output_file_path('deduplicated', 'deduplicated_files')
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.writelines(unique_lines)
    preview_output(unique_lines)
    console.print(f'[green]Duplicate lines removed and saved to {output_file}[/green]')

def filter_by_domain():
    file = file_dialog_single()
    if not file:
        console.print('[red]No file selected![/red]')
        return
    domain = Prompt.ask('Enter the domain (e.g., gmail.com)')
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    filtered_lines = [line for line in lines if domain in line.split('@')[1]]
    output_file = get_output_file_path(f'filtered_{domain}', 'filtered_files')
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.writelines(filtered_lines)
    preview_output(filtered_lines)
    console.print(f"[green]Lines filtered by domain '{domain}' and saved to {output_file}[/green]")

def search_and_replace():
    file = file_dialog_single()
    if not file:
        console.print('[red]No file selected![/red]')
        return
    search_str = Prompt.ask('Enter the string to search for')
    replace_str = Prompt.ask('Enter the string to replace it with')
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    updated_lines = [line.replace(search_str, replace_str) for line in lines]
    output_file = get_output_file_path('search_replace', 'search_replace_files')
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.writelines(updated_lines)
    preview_output(updated_lines)
    console.print(f"[green]Replaced '{search_str}' with '{replace_str}' in all lines. Saved to {output_file}[/green]")

def check_invalid_lines():
    file = file_dialog_single()
    if not file:
        console.print('[red]No file selected![/red]')
        return
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    invalid_lines = [line for line in lines if '@' not in line.split(':')[0] or ':' not in line]
    if invalid_lines:
        output_file = get_output_file_path('invalid_lines', 'invalid_lines_files')
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.writelines(invalid_lines)
        console.print(f'[red]Invalid lines found! Saved invalid lines to {output_file}[/red]')
    else:
        console.print('[green]No invalid lines found in the file![/green]')


def main_menu():
    while True:
        print(banner)
        choice = Prompt.ask(
            "Select an option (1-12) or type 'Quit' to exit"
        )
        if choice == 'Quit':
            console.print("[bold green]Exiting the tool. Goodbye![/bold green]")
            break
        elif choice == '1':
            combine_files()
        elif choice == '2':
            split_file_by_line_or_size()
        elif choice == '3':
            randomize_lines()
        elif choice == '4':
            sort_lines()
        elif choice == '5':
            extract_lines_with_keyword()
        elif choice == '6':
            remove_duplicate_lines()
        elif choice == '7':
            filter_lines_by_domain()
        elif choice == '8':
            convert_url_to_email_password()
        elif choice == '9':
            convert_email_to_user_password()
        elif choice == '10':
            remove_lines_with_keyword()
        elif choice == '11':
            search_and_replace()
        elif choice == '12':
            check_invalid_lines()
        else:
            console.print("[red]Invalid option. Please select again.[/red]")

# Start the main menu
if __name__ == "__main__":
    os.system("cls")
    main_menu()

