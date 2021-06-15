(function () {
    var newsletterElems = document.querySelectorAll(".newsletter");
    newsletterElems.forEach(function (newsletterElem) {
        var form = newsletterElem.querySelector("form");
        var emailElem = form.querySelector("#email");
        var submitButton = form.querySelector("button[type='submit']");
        var checkbox = form.querySelector("#confirm-email");
        var response = form.querySelector("#response");
        form.addEventListener("submit", (event) => {
            event.preventDefault();
            submitButton.setAttribute("disabled", "disabled");
            emailElem.setAttribute("disabled", "disabled");
            checkbox.setAttribute("disabled", "disabled");
            fetch("https://podpri.djnd.si/api/subscribe/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: emailElem.value,
                    segment: 18,
                }),
            })
            .then((res) => {
                if (res.ok) {
                    return res.text();
                }
                throw new Error("Response not ok");
            })
            .then((res) => {
                response.className = "form-text";
                response.textContent = "Hvala za prijavo!";
                console.log(res);
            })
            .catch((error) => {
                console.log(error);
                response.className = "form-text";
                response.textContent = "Napaka pri prijavi :(";
            })
            .then(() => {
                submitButton.removeAttribute("disabled");
                emailElem.removeAttribute("disabled");
                checkbox.removeAttribute("disabled");
            });
        });
    });
})();

(function () {
    var shareLinks = document.querySelectorAll(".socials .social-circle");
    shareLinks.forEach((shareLink) => {
        shareLink.addEventListener("click", function (event) {
            event.preventDefault();
            if (event.currentTarget.className.indexOf('isfbbox') != -1) {
                const url = `https://www.facebook.com/dialog/feed?app_id=301375193309601&redirect_uri=https%3A%2F%2Fhudapobuda.si&link=https%3A%2F%2Fhudapobuda.si&ref=responsive`;
                window.open(url, '_blank');
            }
            if (event.currentTarget.className.indexOf('istwbox') != -1) {
                const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(window.SHARE_TWEET_TEXT + ' https://hudapobuda.si')}`;
                window.open(url, '_blank');
            }
            if (event.currentTarget.className.indexOf('isembox') != -1) {
                const url = `mailto:?subject=HUDA+POBUDA&body=${encodeURIComponent(window.SHARE_EMAIL_TEXT)}`;
                window.open(url, '_blank');
            }
        });
    });
})();

(function () {
    let popup = document.getElementById('filters-mobile');
    let popupButton = document.getElementById('filters-mobile-button');
    let disableBackground = document.getElementById('disable-background');
    if (popupButton) {
        popupButton.addEventListener('click', function() {
            disableBackground.classList.toggle('d-none');
            popup.classList.toggle('closed');
        });
    }
    if (disableBackground) {
        disableBackground.addEventListener('click', function() {
            disableBackground.classList.toggle('d-none');
            popup.classList.toggle('closed');
        });
    }
})();
