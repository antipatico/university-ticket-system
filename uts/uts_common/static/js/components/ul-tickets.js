const TicketsList = {
    components: {
      'li-ticket': TicketListItem,
    },
    props: {
        tickets: Object,
        showOwners: Boolean,
    },
    template: `
    <ul class="list-group list-group-flush">
      <li-ticket :ticket="ticket" :show-owner="showOwners" v-for="ticket in tickets"></li-ticket>
    </ul>`,
}