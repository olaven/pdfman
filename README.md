# pdfman
A tiny "hub" for your folders containing PDF files. 

## Installation 
* `git clone https://github.com/olaven/pdfman.git`
* `chmod +x ./install.sh && ./install.sh`

## Usage 
### You may add "collections": 
* `pdfman add homework ~/Documents/school/homework/`
* `pdfman add books ~/Documents/books/pdfs`
### List collections: 
* `pdfman list`
### Add PDFs to existing collections 
* `pdfman move ./Downloads/lecture01.pdf homework`
* `pdfman move ./Desktop/ulysses.pdf books`
### And, of course, open the files: 
* `pdfman open homework` let's you open PDFs from the homework folder 
* `pdfman open books` let's you open PDFs from the books folder 

