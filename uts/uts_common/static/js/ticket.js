const TicketsApp = {
    delimiters: ['$%', '%$'],
    data() {
        return {
            ticket: null,
        }
    },
    mounted() {
        $.getJSON(API_TICKETS_URL + TICKET_ID + "/", (data) => {
            let owner = data.owner;
            data.events.forEach((e) => {
                if(e.status === "ESCALATION") {
                    e.newOwner = owner;
                    owner = e.owner;
                }
            });
            this.ticket = data;
        });
    },
    methods: {
        f() { return QACommon }
    }
}
Vue.createApp(TicketsApp).mount('#ticketsApp')