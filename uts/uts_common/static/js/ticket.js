const TicketsApp = {
    delimiters: ['$%', '%$'],
    data() {
        return {
            ticket: null,
        }
    },
    mounted() {
        $.getJSON(API_TICKETS_URL + TICKET_ID + "/", (data) => {
            this.ticket = data;
        });
    },
    methods: {
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