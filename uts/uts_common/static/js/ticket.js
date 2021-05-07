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
        f() { return QACommon }
    }
}
Vue.createApp(TicketsApp).mount('#ticketsApp')