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
    dateToString(date) {
        return date.getDate() + "/" + (date.getMonth() + 1) + "/" + date.getFullYear() + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()
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