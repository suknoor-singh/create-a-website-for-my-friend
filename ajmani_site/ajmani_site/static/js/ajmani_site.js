const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector(".site-nav");
const navItemsWithChildren = document.querySelectorAll(".site-nav__item.has-children");
const disclaimerModal = document.querySelector("[data-disclaimer-modal]");
const acceptDisclaimerButton = document.querySelector("[data-accept-disclaimer]");
const closeDisclaimerElements = document.querySelectorAll("[data-close-disclaimer]");
const openDisclaimerElements = document.querySelectorAll("[data-open-disclaimer]");
const disclaimerStorageKey = "ajmani_disclaimer_accepted";
const whatsappWidget = document.querySelector("[data-whatsapp-widget]");
const whatsappToggle = document.querySelector("[data-whatsapp-toggle]");
const whatsappPanel = whatsappWidget?.querySelector(".whatsapp-widget__panel");
const whatsappClose = document.querySelector("[data-whatsapp-close]");
const whatsappInput = document.querySelector("[data-whatsapp-input]");
const whatsappSend = document.querySelector("[data-whatsapp-send]");

if (navToggle && siteNav) {
    navToggle.addEventListener("click", () => {
        const expanded = navToggle.getAttribute("aria-expanded") === "true";
        navToggle.setAttribute("aria-expanded", String(!expanded));
        siteNav.classList.toggle("is-open", !expanded);
    });
}

navItemsWithChildren.forEach((item) => {
    const toggle = item.querySelector(".site-nav__toggle");
    if (!toggle) {
        return;
    }

    toggle.addEventListener("click", () => {
        const expanded = toggle.getAttribute("aria-expanded") === "true";
        toggle.setAttribute("aria-expanded", String(!expanded));
        item.classList.toggle("is-open", !expanded);
    });
});

if (disclaimerModal && acceptDisclaimerButton) {
    const openDisclaimer = () => {
        disclaimerModal.hidden = false;
        document.body.classList.add("has-disclaimer-open");
    };

    const closeDisclaimer = (persistAcceptance = false) => {
        disclaimerModal.hidden = true;
        document.body.classList.remove("has-disclaimer-open");
        if (persistAcceptance) {
            window.localStorage.setItem(disclaimerStorageKey, "true");
        }
    };

    if (window.localStorage.getItem(disclaimerStorageKey) !== "true") {
        openDisclaimer();
    }

    acceptDisclaimerButton.addEventListener("click", () => {
        closeDisclaimer(true);
    });

    closeDisclaimerElements.forEach((element) => {
        element.addEventListener("click", () => {
            closeDisclaimer(false);
        });
    });

    openDisclaimerElements.forEach((element) => {
        element.addEventListener("click", () => {
            openDisclaimer();
        });
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !disclaimerModal.hidden) {
            closeDisclaimer(false);
        }
    });
}

if (whatsappWidget && whatsappToggle && whatsappPanel && whatsappSend) {
    const openWhatsapp = () => {
        whatsappPanel.hidden = false;
        whatsappToggle.setAttribute("aria-expanded", "true");
    };

    const closeWhatsapp = () => {
        whatsappPanel.hidden = true;
        whatsappToggle.setAttribute("aria-expanded", "false");
    };

    whatsappToggle.addEventListener("click", () => {
        if (whatsappPanel.hidden) {
            openWhatsapp();
        } else {
            closeWhatsapp();
        }
    });

    if (whatsappClose) {
        whatsappClose.addEventListener("click", closeWhatsapp);
    }

    whatsappSend.addEventListener("click", () => {
        const baseHref = whatsappSend.getAttribute("href")?.split("?")[0] || "";
        const message = whatsappInput?.value?.trim() || "";
        const nextHref = message ? `${baseHref}?text=${encodeURIComponent(message)}` : baseHref;
        whatsappSend.setAttribute("href", nextHref);
    });
}
