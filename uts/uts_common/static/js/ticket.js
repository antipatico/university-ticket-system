const TicketsApp = {
    delimiters: ['$%', '%$'],
    data() {
        return {
            ticket: null,
            action: "NONE",
            info: null,
            duplicationUrl: null,
            newOwnerEmail: null,
            error: null,
        }
    },
    mounted() {
        $.getJSON(API_TICKETS_URL + TICKET_ID + "/", this.postProcessTicket);
    },
    created() {
        $("#ticketsApp").show();
    },
    computed: {
        TICKET_DETAILS_URL() { return TICKET_DETAILS_URL },
        QACommon() { return QACommon}
    },
    methods: {
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
        handleAPIError(request) {
            this.error = request.responseJSON["detail"];
        },
        actionButtonClick() {
            let data = {
                "ticket_id": TICKET_ID,
                "status": this.action,
                "info": this.info,
            }
            if(this.action === "NONE") {
                this.error = "perfavore seleziona un'azione";
                return;
            }
            if(this.action === "DUPLICATE") {
                if (this.duplicationUrl === null) {
                    this.error = "perfavore inserisci un URL";
                    return;
                }
                let match = this.duplicationUrl.match(/\/([0-9]+)$/);
                if (!match) {
                    this.error = "URL non valido";
                    return;
                }
                data["duplicate_id"] = match[1];
                delete data["info"];
            }

            if(this.action === "ESCALATION") {
                if(this.newOwnerEmail.length < 1) {
                    this.error = "perfavore inserisci l'email del nuovo proprietario";
                    return;
                }
                data["new_owner_email"] = this.newOwnerEmail;
                delete data["info"];
            }
            this.error = null;
            this.info = null;
            this.duplicationUrl = null;
            this.newOwnerEmail = null;
            QACommon.httpJSON("POST", API_TICKET_EVENTS_URL, data, this.postProcessTicket, this.handleAPIError);
        },
    }
}
Vue.createApp(TicketsApp).mount('#ticketsApp')