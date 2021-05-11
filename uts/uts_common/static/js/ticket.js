const TicketsApp = {
    delimiters: ['$%', '%$'],
    data() {
        return {
            ticket: null,
            action: "NONE",
        }
    },
    mounted() {
        $.getJSON(API_TICKETS_URL + TICKET_ID + "/", this.postProcessTicket);
    },
    created() {
        $("#ticketsApp").show();
    },
    methods: {
        f() { return QACommon },
        postProcessTicket(data) {
            let owner = data.owner;
            data.events.forEach((e) => {
                if(e.status === "ESCALATION") {
                    e.newOwner = owner;
                    owner = e.owner;
                }
            });
            this.ticket = data;
        },
        toggleSubscription() {
            let data = {is_subscribed: !this.ticket.is_subscribed};
            QACommon.httpJSON("PATCH", API_TICKETS_URL + TICKET_ID + "/", data, this.postProcessTicket);
        },
        actionButtonClick() {
            switch(this.action) {
                case "NONE":
                    alert("Perfavore seleziona un'azione");
                    return;
                case "ANSWER":

            }
        },
    }
}
Vue.createApp(TicketsApp).mount('#ticketsApp')