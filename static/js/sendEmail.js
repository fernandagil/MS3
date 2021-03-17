function sendMail(contactForm) {
    emailjs.send("gmail", "movieSuggestion", {
        "to_name": contactForm.name.value,
        "to_email": contactForm.emailaddress.value,
        "movie_suggestion": contactForm.moviesuggestion.value
    })
    .then(
        function(response) {
            console.log("SUCCESS", response);
        },
        function(error) {
            console.log("FAILED", error);
        }
    );
    return false;  // To block from loading a new page
}