Generate a csv table from contents of the uploaded document. A PDF and JPG
versions of the same document are provided..

The resulting csv must contain these exact columns: 
- cat_no: (appears as "Cat Nos") values are strings like "FB1003" or "FB3042"
- matrix_no: (appears as "Matrix No.") values are string like "CA14825-1" or
  "W142950"
- date: (appears as "Recorded") values have the format DD.MM.YY.
- title: a record title, such as "I'm Sittin' High on a Hill Top, ft (v) (G.
  Kahn, A.Johnston)"
- artist: for example "The YACHT CLUB BOYS (Adler, Kely, Kem, Manni)"
- notes: various notes that sometimes appear in the cat_no column

## Input document structure

The title and artist appear together in the same column of the document. The
title may include text that looks like artist names but is actually part of the
credits associated with the title. 

To disambiguate titles and artists: 
  - The artist will appear first followed by a series of titles.
  - The artist names often include ALL CAPS sequences (e.g., the last name). 
  - There is usually empty space above each artist/titles block. If there is no
    empty space and you see text that looks like a name, the name may be part of
    a title.
  - The title and artist can span multiple lines. Artist names spanning multiple
    lines are indented but titles are not.

Notes sometimes appear in the cat_no column (the first column). Generally, any
text that does not look like a cat_no ("FB1003" or "FB3042") is a note for the
previous cat_no.

# Additional output requirements
When a cat_no appears to be missing, repeat the previous value. 

The csv output should always use quotes for the title and artist

cat_no, matrix_no, date, title, and artists should never be empty. If a title or
artist appears to be empty, reconsider instructions to disambiguate titles and
artists. Go back and check if there is text in the input that is not included in
the csv output. If you still can't determine the value, leave it empty in the
csv.

Include all titles and artists from the input in the output.

Wrap generated csv in a markdown code block like this:

```csv
"cat_no","matrix_no","date","title","artist","notes"
"FB1000","CA14826-1","14.12.34","I'm In Love, ft. (Simon, Mysels) (v) Harry Jacobson","Carroll GIBBONS and The SAVOY HOTEL ORPHEANS",""
"FB1000","CA14824-1","14.12.34","Dancing on a Dime, ft (Sievier, Ramsay) (v) Anne Lenner","Carroll GIBBONS and The SAVOY HOTEL ORPHEANS",""
```

