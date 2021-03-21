function sendWelcomeEmail(loginForm) {
    emailjs.send("gmail", "signinConfirmation", {
        "from_name": loginForm.username.value,
        "from_email": loginForm.email.value,
    })
    .then(
        function(response) {
            console.log("SUCCESS", response);
        },
        function(error) {
            console.log("FAILED", error);
        }
    );
}

function sendMail(contactForm) {
    emailjs.send("gmail", "movieSuggestion", {
        "from_name": contactForm.name.value,
        "from_email": contactForm.emailaddress.value,
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