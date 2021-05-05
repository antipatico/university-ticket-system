const TicketsApp = {
    delimiters: ['$%', '%$'],
    components: {
      'li-ticket': TicketListItem,
    },
    data() {
        return {
            recentTickets: null,
            ownedTickets: null,
            subscribedTickets: null,
        }
    },
    created() {
        $("#ticketsApp").show();
    },
    mounted() {
        this.recentTicketsTimer = QACommon.interval(this.getRecentTickets, 20 * 1000);
        this.ownedTicketsTimer = QACommon.interval(this.getOwnedTickets, 5 * 60 * 1000);
        this.subscribedTicketsTimer = QACommon.interval(this.getSubscribedTickets, (5 * 60 * 1000) + 200);
    },
    methods: {
        getRecentTickets() {
            $.getJSON(API_RECENT_ACTIVITIES_URL, (data) => {
                this.recentTickets = data;
            });
        },
        getOwnedTickets() {
            $.getJSON(API_TICKETS_URL, (data) => {
                this.ownedTickets = data;
            });
        },
        getSubscribedTickets() {
            $.getJSON(API_SUBSCRIBED_TICKETS_URL, (data) => {
                this.subscribedTickets = data;
            });
        },
    }
}
const app = Vue.createApp(TicketsApp);

app.mixin({
    methods: {
        getIconClass(status) {
            return QACommon.getIconClass(status);
        },
        getEventMessage(status) {
            return QACommon.getEventMessage(status);
        },
        dateToString(date) {
            return QACommon.dateToString(date);
        },
        dateDiffFromNow(date) {
            date = new Date(date);
            let now = new Date();
            let secondsDiff = (now - date) / 1000;
            if (secondsDiff < 10) {
                return "ora";
            } else if (secondsDiff < 60) {
                return `${secondsDiff} secondi fa`;
            } else {
                let minutesDiff = secondsDiff / 60;
                if (minutesDiff < 2) {
                    return "un minuto fa";
                } else if (minutesDiff < 60) {
                    return `${minutesDiff} minuti fa`;
                } else {
                    let hoursDiff = minutesDiff / 60;
                    if (hoursDiff < 2) {
                        return "un'ora fa";
                    } else if (hoursDiff < 24) {
                        return `${hoursDiff} ore fa`;
                    } else {
                        let daysDiff = hoursDiff / 24;
                        if (daysDiff < 2) {
                            return "un giorno fa";
                        } else if (daysDiff < 30) {
                            return `${daysDiff} giorni fa`;
                        } else {
                            let monthsDiff = daysDiff / 30;
                            if (monthsDiff < 2) {
                                return "un mese fa";
                            } else if (monthsDiff < 12) {
                                return `${monthsDiff} mesi fa`
                            } else {
                                let yearsDiff = monthsDiff / 12;
                                if (monthsDiff < 2) {
                                    return "un anno fa";
                                }
                                return `${yearsDiff} anni fa`;
                            }
                        }
                    }
                }
            }
        },
        openTicketDetails(ticketId) {
            window.location.href = TICKET_DETAILS_URL + ticketId
        },
    }
});

app.mount("#ticketsApp");