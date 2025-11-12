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
  Text that looks like artist names is sometimes included in the title value but
  these are credits associated the title. To disambiguate titles and artists:
  The artist will appear first followed by a series of titles. There is always
  empty space above each artist/titles block. When there is no empty space and
  you see text that looks like a name, the name is actually part of a title.
- The title and artist can span multiple lines. Artist names spanning multiple
  lines are indented but titles are not.
- Notes sometimes appear in the "Cat Nos" column (the first column). Generally,
  any text that does not look like a Cat No ("FB1003" or "FB3042") is a note for
  the preceding Cat No.
- When a Cat No appears to be missing, repeat the previous value. 
- The csv output should always use quotes for the title and artist
- cat_no, matrix_no, date, title, and artists should never be empty. If a title
  or artist appears to be empty, reconsider instructions to disambiguate titles
  and artists. Go back and check if there is text in the PDF that is not
  included in the csv output. If you still can't determine the value, leave it
  empty in the csv.
- Include all titles and artists from the PDF in the output.

Here are example artist names (some span multiple lines with indentation in the pdf)

- HILDEGARDE - The Irresistible Singer, with Orchestra
- The B.B.C. DANCE ORCHESTRA, directed by Henry HALL
- Les ALLEN and His CANADIAN BACHELORS with Novelty Accomp.
- MASSED BANDS, ROYAL MARINES (Portsmouth) conductor, Bandmaster G.C. KEEN
- FLANAGAN and ALLEN - The "Oi" comedians

Here are example titles (some span multiple lines):

- The Snowy Breasted Pearl (S.E. De Vere, J.Robinson) Sam CARSON, baritone
  (=Dr.Griffiths, M.D.) with violin, cello and the Compton theatre organ in
  Studio 1A Abbey Road, NW
- A Beautiful Lady in Blue (S. Lewis, J.F. Coots)
- London Pride - Part. 1 Cockneys at Heart (A.A.Thomson, Ashley, Sterne)