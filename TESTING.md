# Testing

- <a href="#1">1. Code Validators</a>
- <a href="#2">2. Responsiveness</a>

<span id="#1"></span>
## 1. Code validators

### [HTML Validator](https://validator.w3.org/) : 
While testing the HTML code, I had some errors related to Jinja templating. These errors were omitted for the correct functioning of the site. Some examples:
![](readme-files/html-jinja.jpg)

Apart from these, the test returned some errors and warnings not related to Jinja: 

###### Movie Page
After passing the page through the HTML Validator, and after checking for non Jinja related errors, this <p> tag related error was found. 
When I went to the code to fix the error I saw that the opening <p> tag was actually there, so this error was ignored.

![](readme-files/html-movies.jpg)

###### Add New Movie Page and Edit Movie Page
This two pages returned the same errors since it was the same form, just adjusted for each site needs.
![](readme-files/html-addmovie.jpg)
![](readme-files/html-editmovie.jpg)

- The <h4>, maxlength and minlegth related error were fixed by ommiting them since they weren't necessary for the correct functioning of the site nor didn't affect the styling.
- The for attribute related errors were fixed by including the missing ID element in the <input> field below the <labels>.

### [CSS Validator](https://jigsaw.w3.org/css-validator/) : 

The test returned some warnings related to some browser cross-compatibility. They were ignored in order to have the content render properly on every browser.

![](readme-files/css-warning.jpg)

#### [JSHint JavaScript Validator](https://jshint.com/) :
The test returned two type of warnings:
- one undefined variable 
- two unused variables: this is a function called from outside the **script.js** file

![](readme-files/js-validator.jpg)

### [PEP8 Python Validator](http://pep8online.com/) : 
The test returned some errors and warnings. All of them were fixed following the recommendations.

![](readme-files/python-validator.jpg)

---

<span id="#2"></span>
## 2. Responsiveness
To test the responsiveness of the site I used [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools) and [Responsive Design Checker](https://www.responsivedesignchecker.com/).
I also asked some family members and friends to test it on their devices.




---

[Go back to README.md file](README.md).