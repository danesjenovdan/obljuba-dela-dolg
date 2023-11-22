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
            if (checkbox.checked) {
                form.classList.remove("error");
                submitButton.setAttribute("disabled", "disabled");
                emailElem.setAttribute("disabled", "disabled");
                checkbox.setAttribute("disabled", "disabled");
                fetch("https://podpri.lb.djnd.si/api/subscribe/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        email: emailElem.value,
                        segment_id: 23,
                    }),
                })
                .then((res) => {
                    if (res.ok) {
                        return res.text();
                    }
                    throw new Error("Response not ok");
                })
                .then((res) => {
                    response.className = "form-text text-start";
                    response.textContent = "Hvala za prijavo!";
                    console.log(res);
                })
                .catch((error) => {
                    console.log(error);
                    response.className = "form-text text-start text-error";
                    response.textContent = "Napaka pri prijavi :(";
                })
                .then(() => {
                    submitButton.removeAttribute("disabled");
                    emailElem.removeAttribute("disabled");
                    checkbox.removeAttribute("disabled");
                });
            } else {
                form.classList.add("error");
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

(function () {
    var header = document.getElementsByClassName("header")[0];
    document.addEventListener('scroll', function(e) {
        // console.log('scroll');
        // console.log(window.scrollY);
        if (window.scrollY > 0) {
            header.classList.add('scrolling');
        } else {
            header.classList.remove('scrolling');
        }
    });
})();

function selectCategory() {
    document.getElementById("search-header").value = '';
    document.getElementById("query-form").submit();
}

function selectStatus() {
    // let category = document.getElementById("select-category").value;
    // let query = document.getElementById("search-header").value;
    // TODO: porihti za mobile
    let popup = document.getElementById('filters-mobile');
    // let status = popup.getElementsByClassName("active")[0].dataset.status;
    // window.location.href = '?kategorija=' + category + '&isci=' + query + '&status=' + status;
    document.getElementById("query-form").submit();
}

function readMore(event, id) {
    if (id) {
        let updateContent = document.getElementById(id);
        updateContent.classList.toggle('d-none');

        let button = event.target;

        if (!button.classList.contains('read-more')) {
            button = button.parentElement;
        }
        
        button.classList.toggle('close');

        if (button.classList.contains('close')) {
            if (id !== 'coalition-contract' && id !== 'party-mobile') {
                button.firstElementChild.textContent = 'Zapri';
            }
            
        } else {
            if (id !== 'coalition-contract' && id !== 'party-mobile') {
                button.firstElementChild.textContent = 'Preberi celotno analizo';
            }
            
        }
        
    }
}
