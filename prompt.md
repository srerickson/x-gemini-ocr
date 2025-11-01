Generate csv table for the table in the uploaded PDF.

The table must contain these exact columns: 
- cat_no: (appears as "Cat Nos") values are strings like "FB1003" or "FB3042"
- matrix_no: (appears as "Matrix No.") values are string like "CA14825-1" or "W142950"
- date: (appears as "Recorded") values have the format DD.MM.YY.
- title: a record title, such as "I'm Sittin' High on a Hill Top, ft (v) (G. Kahn, A.Johnston)"
- artist: for example "The YACHT CLUB BOYS (Adler, Kely, Kem, Manni)"
- notes: various notes that sometimes appear in the cat_no column

Please follow these critical formatting rules to ensure accuracy:

- The title and artist appear together in the same vertical column in the PDF.
  The artist will appear first followed by lines with record titles.
- Notes sometimes appear in the "Cat Nos" column (the first column). Generally,
  any text that does not look like a Cat No ("FB1003" or "FB3042") is a note for
  the preceding Cat No.
- When a Cat No appears to be missing, repeat the previous value. 
- The csv output should always use quotes for the title and artist