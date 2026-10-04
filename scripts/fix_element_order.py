import docx
import shutil

src = 'Journal_Paper_Indri_Anjar_MBG_SNA_JIKI_REVISED.docx'
doc = docx.Document(src)
body = doc._body._body

# Find elements by text or tag
h45 = None
narr45 = None
cap_t5 = None
tbl5 = None
narr_t6 = None
cap_t6 = None
tbl6 = None
img_fig9 = None
cap_fig9 = None
img_fig10 = None
cap_fig10 = None
narr_net_nlp = None
h46 = None
narr46 = None
cap_t7 = None
tbl7 = None
h5 = None

for child in list(body):
    txt = ''.join(child.itertext()).strip()
    if child.tag.endswith('p'):
        if '4.5\tModel Evaluation and Benchmark' in txt or '4.5 Model Evaluation and Benchmark' in txt:
            h45 = child
        elif 'To establish empirical classification validity' in txt:
            narr45 = child
        elif txt.startswith('Table 5.'):
            cap_t5 = child
        elif 'Table 6 details the class-wise performance breakdown' in txt:
            narr_t6 = child
        elif txt.startswith('Table 6.'):
            cap_t6 = child
        elif 'Figure 9. Normalized confusion matrix' in txt:
            cap_fig9 = child
        elif 'Figure 10. Class-wise F1-scores' in txt:
            cap_fig10 = child
        elif 'Directly evaluating the relationship between network positions and NLP affective' in txt:
            narr_net_nlp = child
        elif '4.6\tLongitudinal Network Dynamics' in txt or '4.6 Longitudinal Network Dynamics' in txt:
            h46 = child
        elif 'To evaluate whether the observed network hyper-fragmentation and affective' in txt:
            narr46 = child
        elif txt.startswith('Table 7.'):
            cap_t7 = child
        elif '5\tDiscussion' in txt or '5 Discussion' in txt:
            h5 = child
        else:
            drawings = child.xpath('.//a:blip')
            if drawings:
                embed_id = drawings[0].attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                if embed_id == 'rId63':
                    img_fig9 = child
                elif embed_id == 'rId66':
                    img_fig10 = child
    elif child.tag.endswith('tbl'):
        tbl_txt = ''.join(child.itertext())
        if 'Partition Protocol' in tbl_txt:
            tbl5 = child
        elif 'Class Share (%)' in tbl_txt:
            tbl6 = child
        elif 'Longitudinal Shift & Sociological Meaning' in tbl_txt:
            tbl7 = child

print("Elements found:")
print("h45:", h45 is not None)
print("narr45:", narr45 is not None)
print("cap_t5:", cap_t5 is not None)
print("tbl5:", tbl5 is not None)
print("narr_t6:", narr_t6 is not None)
print("cap_t6:", cap_t6 is not None)
print("tbl6:", tbl6 is not None)
print("img_fig9:", img_fig9 is not None)
print("cap_fig9:", cap_fig9 is not None)
print("img_fig10:", img_fig10 is not None)
print("cap_fig10:", cap_fig10 is not None)
print("narr_net_nlp:", narr_net_nlp is not None)
print("h46:", h46 is not None)
print("narr46:", narr46 is not None)
print("cap_t7:", cap_t7 is not None)
print("tbl7:", tbl7 is not None)
print("h5:", h5 is not None)

ordered_elements = [
    h45,
    narr45,
    cap_t5,
    tbl5,
    narr_t6,
    cap_t6,
    tbl6,
    img_fig9,
    cap_fig9,
    img_fig10,
    cap_fig10,
    narr_net_nlp,
    h46,
    narr46,
    cap_t7,
    tbl7
]

if all(e is not None for e in ordered_elements) and h5 is not None:
    curr = h45
    for el in ordered_elements[1:]:
        curr.addnext(el)
        curr = el
    print("SUCCESS: Perfectly re-ordered Section 4.5 and 4.6 elements!")
else:
    print("Warning: some elements were not found!")

doc.save('Journal_Paper_Indri_Anjar_MBG_SNA_JIKI_REVISED.docx')
shutil.copyfile('Journal_Paper_Indri_Anjar_MBG_SNA_JIKI_REVISED.docx', '/Users/jevin/Downloads/Journal_Paper_Indri_Anjar_MBG_SNA_JIKI.docx')
print("Saved and updated Downloads folder!")
