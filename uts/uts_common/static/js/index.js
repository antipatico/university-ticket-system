
function interval(f,delay) {
    f();
    return setInterval(f, delay);
}

const TicketsApp = {
    delimiters: ['$%','%$'],
    data() {
        return {
            openedTicket: null,
            recentTickets: null,
        }
    },
    mounted() {
        this.recentTicketsTimer = interval(this.getRecentTickets, 60*1000);
    },
    methods: {
        getRecentTickets() {
            $.getJSON("/api/v1/recentactivities/", (data) => {
                this.recentTickets = data;
            });
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
        }
    }
}
Vue.createApp(TicketsApp).mount('#ticketsApp')