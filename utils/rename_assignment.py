"""
Script to rename assignment output files with unified naming convention.
Format: CourseName_AssignmentNo_StudentName_StudentID.pdf
"""

import yaml
import argparse
from pathlib import Path
import shutil


def read_metadata(metadata_path):
    """Read course and student information from _metadata.yml"""
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)
    return metadata


def sanitize_filename(text):
    """Remove or replace characters that are not suitable for filenames"""
    # Replace spaces with underscores
    text = text.replace(' ', '_')
    # Remove special characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        text = text.replace(char, '')
    return text


def rename_output_file(assignment_folder, output_filename=None):
    """
    Rename the output file based on metadata and folder structure.
    
    Args:
        assignment_folder: Path to the assignment folder (e.g., 'MIN-E-630/HW-1')
        output_filename: Name of the output file to rename (default: 'hw-1.pdf')
    """
    assignment_path = Path(assignment_folder)
    
    # Find _quarto.yml in the root directory (workspace root)
    root_path = assignment_path.parent.parent
    quarto_path = root_path / '_quarto.yml'
    
    if not quarto_path.exists():
        print(f"Error: _quarto.yml not found at {quarto_path}")
        return False
    
    # Read metadata
    try:
        quarto_config = read_metadata(quarto_path)
    except Exception as e:
        print(f"Error reading metadata: {e}")
        return False
    
    # Extract information
    course_folder_name = assignment_path.parent.name  # e.g., 'MIN-E-630'
    course_name = quarto_config.get('courses', {}).get(course_folder_name, course_folder_name)
    assignment_no = assignment_path.name  # Use folder name as assignment number
    student_name = quarto_config.get('student', {}).get('name', 'UNKNOWN')
    student_id = quarto_config.get('student', {}).get('id', 'UNKNOWN')
    
    # Sanitize all components
    course_name = sanitize_filename(course_name)
    assignment_no = sanitize_filename(assignment_no)
    student_name = sanitize_filename(student_name)
    student_id = sanitize_filename(str(student_id))
    
    # Find the output file
    if output_filename:
        output_path = assignment_path / output_filename
        if not output_path.exists():
            print(f"Error: Output file not found at {output_path}")
            return False
    else:
        # Auto-detect PDF file
        pdf_files = list(assignment_path.glob('*.pdf'))
        # Exclude already renamed files
        pdf_files = [f for f in pdf_files if not ('_' in f.stem and len(f.stem.split('_')) >= 5)]
        
        if not pdf_files:
            print(f"Error: No PDF files found in {assignment_path}")
            return False
        
        output_path = pdf_files[0]
        print(f"Found output file: {output_path.name}")
    
    # Get file extension
    file_ext = output_path.suffix
    
    # Create new filename
    new_filename = f"{course_name}_{assignment_no}_{student_name}_{student_id}{file_ext}"
    new_path = assignment_path / new_filename
    
    # Rename the file
    try:
        shutil.move(str(output_path), str(new_path))
        print(f"Successfully renamed:")
        print(f"  From: {output_path.name}")
        print(f"  To:   {new_filename}")
        print(f"  Path: {new_path}")
        return True
    except Exception as e:
        print(f"Error renaming file: {e}")
        return False


def detect_assignment_folder():
    """Detect assignment folder from environment or current working directory"""
    # First check current working directory
    cwd = Path.cwd()
    print(f"DEBUG: Current working directory = {cwd}")
    
    # Check if we're in an assignment folder (parent parent has _quarto.yml)
    root_quarto = cwd.parent.parent / '_quarto.yml'
    if root_quarto.exists():
        print(f"DEBUG: CWD is assignment folder (found _quarto.yml at {root_quarto})")
        return cwd
    
    # Check if cwd is the project root and find the most recently modified PDF
    project_quarto = cwd / '_quarto.yml'
    if project_quarto.exists():
        print(f"DEBUG: CWD is project root, searching for recently modified PDF")
        
        # Find all PDF files in course/assignment folders
        newest_pdf = None
        newest_time = 0
        
        for course_folder in cwd.iterdir():
            if course_folder.is_dir() and not course_folder.name.startswith(('.', '_')):
                for assignment_folder in course_folder.iterdir():
                    if assignment_folder.is_dir() and not assignment_folder.name.startswith(('.', '_')):
                        for pdf_file in assignment_folder.glob('*.pdf'):
                            mtime = pdf_file.stat().st_mtime
                            if mtime > newest_time:
                                newest_time = mtime
                                newest_pdf = pdf_file
        
        if newest_pdf:
            assignment_folder = newest_pdf.parent
            print(f"DEBUG: Found most recent PDF at {newest_pdf}")
            print(f"DEBUG: Using assignment folder {assignment_folder}")
            return assignment_folder
    
    print("ERROR: Could not detect assignment folder from environment")
    return None


def main():
    """Main function to handle command line arguments or Quarto post-render"""
    parser = argparse.ArgumentParser(
        description='Rename assignment output files with unified naming convention'
    )
    parser.add_argument(
        'rendered_file',
        nargs='?',  # Make it optional
        help='Path to the rendered file (passed by Quarto) or assignment folder'
    )
    parser.add_argument(
        '-f', '--filename',
        help='Output filename to rename (if not specified, will use rendered file name)'
    )
    
    args = parser.parse_args()
    
    # Determine assignment folder and output filename
    if args.rendered_file:
        rendered_path = Path(args.rendered_file)
        print(f"DEBUG: Rendered file = {rendered_path}")
        
        # If it's a file (e.g., hw-1.pdf), use its parent as assignment folder
        if rendered_path.is_file():
            assignment_folder = str(rendered_path.parent)
            output_filename = rendered_path.name if not args.filename else args.filename
            print(f"Auto-detected from rendered file:")
            print(f"  Assignment folder: {assignment_folder}")
            print(f"  Output file: {output_filename}")
        # If it's a directory, use it as assignment folder
        elif rendered_path.is_dir():
            assignment_folder = str(rendered_path)
            output_filename = args.filename
        else:
            print(f"Error: Rendered file not found: {rendered_path}")
            exit(1)
    else:
        # Auto-detect when no argument provided
        detected = detect_assignment_folder()
        if detected:
            assignment_folder = str(detected)
            print(f"Auto-detected assignment folder: {assignment_folder}")
            output_filename = args.filename
        else:
            print("Error: Could not detect assignment folder. Please provide it as an argument.")
            exit(1)
    
    success = rename_output_file(assignment_folder, output_filename)
    
    if success:
        print("\n[SUCCESS] File renamed successfully!")
    else:
        print("\n[ERROR] Failed to rename file.")
        exit(1)


if __name__ == '__main__':
    main()
