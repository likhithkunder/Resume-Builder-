document.addEventListener("DOMContentLoaded", function () {
    const notifications = document.querySelector(".notifications");
    const buttons = document.querySelectorAll(".btn-contact, .generate-resume-btn");

    // Function to disable all buttons
    const disableButtons = () => {
        buttons.forEach(button => {
            button.disabled = true;
        });
    }

    // Function to enable all buttons
    const enableButtons = () => {
        buttons.forEach(button => {
            button.disabled = false;
        });
    }

    const toastDetails = {
        timer: 2000,
        success: {
            icon: 'fa-circle-check',
            text: 'Success: ' + information + '.',
        },
        error: {
            icon: 'fa-circle-xmark',
            text: 'Error: ' + information + '.',
        },
        warning: {
            icon: 'fa-triangle-exclamation',
            text: 'Warning: ' + information + '.',
        },
        info: {
            icon: 'fa-circle-info',
            text: 'Info: ' + information + '.',
        }
    }

    const removeToast = (toast) => {
        toast.classList.add("hide");
        if (toast.timeoutId) clearTimeout(toast.timeoutId);
        setTimeout(() => {
            toast.remove();
            enableButtons(); // Enable buttons after the toast disappears
        }, 500);
    }

    const createToast = (id) => {
        const existingToast = document.querySelector(`.toast.${id}`);

        if (!existingToast) {
            disableButtons(); // Disable buttons when the toast is created

            const { icon, text } = toastDetails[id];
            const toast = document.createElement("li");
            toast.className = `toast ${id}`;
            toast.innerHTML = `<div class="column">
                                 <i class="fa-solid ${icon}"></i>
                                 <span>${text}</span>
                              </div>
                              <i class="fa-solid fa-xmark" onclick="removeToast(this.parentElement)"></i>`;
            notifications.appendChild(toast);

            toast.timeoutId = setTimeout(() => removeToast(toast), toastDetails.timer);
        }
    }

    createToast(messages);
});
