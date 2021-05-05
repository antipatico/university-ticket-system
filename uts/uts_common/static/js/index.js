const TicketsApp = {
    delimiters: ['$%', '%$'],
    data() {
        return {
            recentTickets: null,
            ownedTickets: null,
            subscribedTickets: null,
        }
    },
    mounted() {
        this.recentTicketsTimer = QACommon.interval(this.getRecentTickets, 20 * 1000);
        this.ownedTicketsTimer = QACommon.interval(this.getOwnedTickets, 5 * 60 * 1000);
        this.subscribedTicketsTimer = QACommon.interval(this.getSubscribedTickets, (5 * 60 * 1000) + 200);
    },
    methods: {
        openTicketDetails(ticketId) {
            window.location.href = TICKET_DETAILS_URL + ticketId
        },
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
        getIconClass(status) {
            return QACommon.getIconClass(status);
        },
        getEventMessage(status) {
            return QACommon.getEventMessage(status);
        },
        dateToString(date) {
            return QACommon.dateToString(date);
        }
    }
}
Vue.createApp(TicketsApp).mount('#ticketsApp')