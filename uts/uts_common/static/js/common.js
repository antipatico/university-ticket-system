const QACommon = {
    interval(f, delay) {
        f();
        return setInterval(f, delay);
    },
    getIconClass(status) {
        switch (status) {
            case "OPEN":
                return "bi-envelope-open"
            case "CLOSED":
                return "bi-envelope"
            case "DUPLICATE":
                return "bi-intersect"
            case "ESCALATION":
                return "bi-file-earmark-person"
            case "NOTE":
                return "bi-vector-pen"
            case "INFO_NEEDED":
                return "bi-info-circle"
            case "ANSWER":
                return "bi-award"
        }
    },
    getEventMessage(status) {
        switch (status) {
            case "OPEN":
                return "ha aperto il ticket"
            case "CLOSED":
                return "ha chiuso il ticket"
            case "DUPLICATE":
                return "ha marcato il ticket come duplicato"
            case "ESCALATION":
                return "ha passato la proprietà del ticket"
            case "NOTE":
                return "ha aggiunto una nota"
            case "INFO_NEEDED":
                return "ha richiesto informazioni aggiuntive"
            case "ANSWER":
                return "ha risposto"
        }
    },
    getStatusName(status) {
        switch (status) {
            case "OPEN":
                return "Aperto"
            case "CLOSED":
                return "Chiuso"
            case "DUPLICATE":
                return "Duplicato"
            case "ESCALATION":
                return "Trasferito"
            case "NOTE":
                return "Annotato"
            case "INFO_NEEDED":
                return "Incompleto"
            case "ANSWER":
                return "Risposto"
        }
    },
    dateToString(date) {
        return date.getDate() + "/" + (date.getMonth() + 1) + "/" + date.getFullYear() + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()
    },
    dateDiffFromNow(date) {
        let delta = new Date() - new Date(date); // difference between now and  the date passed in milliseconds
        if (delta >= 6.307e10) { // delta >= 2 years
            return `${Math.trunc(delta / 3.154e10)} anni fa`;
        }
        if (delta >= 3.154e10) { // delta >= 1 year
            return "un anno fa";
        }
        if (delta >= 5.256e9) { // delta >= 2 months
            return `${Math.trunc(delta / 2.628e9)} mesi fa`;
        }
        if (delta >= 2.628e9) { // delta >= 1 month
            return "un mese fa";
        }
        if (delta >= 1.21e9) { // delta >= 2 weeks
            return `${Math.trunc(delta / 6.048e8)} settimane fa`
        }
        if (delta >= 6.048e8) { // delta >= 1 week
            return "una settimana fa";
        }
        if (delta >= 1.728e8) { // delta >= 2 days
            return `${Math.trunc(delta / 8.64e7)} giorni fa`;
        }
        if (delta >= 8.64e7) { // delta >= 1 day
            return "un giorno fa";
        }
        if (delta >= 7.2e6) { // delta >= 2 hours
            return `${Math.trunc(delta/3.6e6)} ore fa`;
        }
        if (delta >= 3.6e6) { // delta >= 1 hour
            return "un'ora fa";
        }
        if (delta >= 120000) { // delta >= 2 minutes
            return `${Math.trunc(delta / 60000)} minuti fa`;
        }
        if (delta >= 60000) { // delta >= 1 minute
            return "un minuto fa";
        }
        return "qualche secondo fa";
    }
}


/* Local login script */
$("#btn-login").click((e) => {
    if (e.shiftKey) {
        e.preventDefault();
        window.location.href = LOCAL_LOGIN_URL;
    }
});

$(window).on("keyup keydown", (e) => {
    if (e.keyCode === 16) {
        $('#btn-login .btn').toggleClass("btn-primary btn-danger");
    }
});