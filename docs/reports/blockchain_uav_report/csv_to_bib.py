'''
import csv
import re

def generate_bibtex_entry(row):
    try:
        # Create a unique citation key
        authors = row["Authors (ordered)"]
        year = row["Exact Date"].split('/')[-1]
        title_words = re.findall(r'\w+', row["Title"])
        if "et al." in authors:
            first_author = authors.split(" ")[0]
        else:
            first_author = authors.split(";")[0].split(",")[0].strip()
        
        if not first_author:
            first_author = "Unknown"

        citation_key = f'{first_author.lower().replace(" ", "")}{year}{title_words[0].capitalize()}'

        # Determine entry type
        paper_type = row["Paper type"].lower()
        if "journal" in paper_type or "review" in paper_type:
            entry_type = "@article"
        elif "preprint" in paper_type:
            entry_type = "@misc" # or @article with journal="arXiv"
        else:
            entry_type = "@inproceedings"

        # Build BibTeX entry
        bib_entry = f'{entry_type}{{{citation_key},\n'
        bib_entry += f'  title={{{row["Title"]}}},\n'
        bib_entry += f'  author={{{authors.replace(";", " and ")}}},\n'
        if entry_type == "@article":
            bib_entry += f'  journal={{{row["Venue"]}}},\n'
        elif entry_type == "@inproceedings":
            bib_entry += f'  booktitle={{{row["Venue"]}}},\n'
        else: # misc for preprints
            bib_entry += f'  howpublished={{arXiv preprint}},\n'
            if row.get("DOI") and "arXiv" in row["DOI"]:
                bib_entry += f'  eprint={{{row["DOI"]}}},\n'

        bib_entry += f'  year={{{year}}},\n'
        if row.get("DOI") and "arXiv" not in row["DOI"]:
            bib_entry += f'  doi={{{row["DOI"]}}},\n'
        if row.get("Stable URLs"):
            bib_entry += f'  url={{{row["Stable URLs"]}}},\n'
        bib_entry += "}\n"

        return bib_entry
    except Exception as e:
        print(f"Error processing row: {row}")
        print(f"Error: {e}")
        return None


try:
    with open('/home/ubuntu/upload/blockchain_uav_biblio_50_verified.csv', 'r') as infile, \
         open('/home/ubuntu/blockchain_uav_report/references.bib', 'w') as outfile:
        reader = csv.DictReader(infile)
        print("Processing CSV file...")
        for i, row in enumerate(reader):
            # print(f"Processing row {i+1}")
            bib_entry = generate_bibtex_entry(row)
            if bib_entry:
                outfile.write(bib_entry)
                outfile.write("\n")

    print("BibTeX file generated successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

'''
