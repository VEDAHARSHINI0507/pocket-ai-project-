document.addEventListener("DOMContentLoaded", function () {

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function () {

            const button = form.querySelector(
                "button[type='submit']"
            );

            if (button) {

                button.disabled = true;

                button.textContent =
                    "Generating...";

            }

        });

    });


    const alerts = document.querySelectorAll(
        ".error-message"
    );

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.style.opacity = "0";

            setTimeout(function () {
                alert.remove();
            }, 300);

        }, 5000);

    });

});