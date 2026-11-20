# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""Updates Open Data Pakistan provenance link and metadata in scratch/build_master_handbook.py."""

with open('scratch/build_master_handbook.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Historical Corpus paragraph
old_corpus = '''            "The raw dataset is stored at <font name='Courier'>data/raw/elections.csv</font>. "
            "It compiles 24,585 candidate records spanning 11 general elections: 1970, 1977, 1988, 1990, 1993, 1997, 2002, 2008, 2013, 2018, and 2024. "
            "This historical corpus represents official Election Commission of Pakistan (ECP) gazette returns digitized across five decades.",'''

new_corpus = '''            "The raw dataset is stored at <font name='Courier'>data/raw/elections.csv</font>. "
            "It is officially sourced from <b>Open Data Pakistan</b> (Resource ID: <font name='Courier'>9e385875-efa0-4f58-aa8c-c2bac028b086</font>): "
            "<br/><font color='#0284c7'><u>https://opendata.com.pk/dataset/pakistan-general-elections-1970-2024/resource/9e385875-efa0-4f58-aa8c-c2bac028b086</u></font>. "
            "<br/>This public dataset compiles 24,585 candidate records spanning 11 national general elections: "
            "1970, 1977, 1988, 1990, 1993, 1997, 2002, 2008, 2013, 2018, and 2024. "
            "The corpus represents digitized official Election Commission of Pakistan (ECP) gazette returns across five decades.",'''

if old_corpus in content:
    content = content.replace(old_corpus, new_corpus)
    print("Replaced Historical Corpus paragraph.")
else:
    print("Could not find old_corpus.")

# Replace Model Card Training Dataset row
old_mcard = '''[Paragraph("Training Dataset", tbl_text), Paragraph("15,879 candidate records spanning 1970 to 2013 general elections (9 elections)", tbl_text)],'''
new_mcard = '''[Paragraph("Training Dataset", tbl_text), Paragraph("15,879 records (1970–2013) from Open Data Pakistan (Resource ID: 9e385875-efa0-4f58-aa8c-c2bac028b086)", tbl_text)],'''

if old_mcard in content:
    content = content.replace(old_mcard, new_mcard)
    print("Replaced Model Card row.")
else:
    print("Could not find old_mcard.")

with open('scratch/build_master_handbook.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated build_master_handbook.py successfully.")
