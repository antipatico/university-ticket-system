const TicketListItem = {
    props: {
        ticket: Object
    },
    template: `
<li class="list-group-item">
  <div class="row">
    <div class="col-md-8">
          <span v-if="ticket.is_closed" class="click bi text-muted" :class="getIconClass(ticket.status)"  v-on:click="openTicketDetails(ticket.id)">&nbsp;<del>{{ticket.name}}</del></span>
          <span v-else class="click bi" :class="getIconClass(ticket.status)"  v-on:click="openTicketDetails(ticket.id)">&nbsp;<strong>{{ticket.name}}</strong></span>
      </div>
    <div class="col-md-4">
      <small>Aperto {{dateDiffFromNow(ticket.ts_open)}}</small>
    </div>
  </div>
</li>`,
}