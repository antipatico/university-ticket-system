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
            $.ajax(API_TICKETS_URL + TICKET_ID + "/", {
                type: "PATCH",
                dataType: "json",
                data: JSON.stringify(data),
                contentType: "application/json",
                headers: {'X-CSRFToken': csrftoken},
            }).done((data) => {
                this.postProcessTicket(data);
            });
        },
    }
}
Vue.createApp(TicketsApp).mount('#ticketsApp')