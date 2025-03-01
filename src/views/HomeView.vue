<script setup>
import { onBeforeMount } from "vue";
import NavBar from "../components/NavBar.vue";
import { ref } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css"

const homepageInfo = {
  data: ref({}),
  get title() {
    return this.data.value.title ?? "Baby Shower"
  },
  get subtitle() {
    return this.data.value.subtitle ?? ""
  },

  get eventDatetime() {
    if (this.data.value.datetime !== undefined) {
      return new Date(this.data.value.datetime)
    } else {
      return undefined
    }
  },
  get eventDate() {
    return (
      this.eventDatetime
      ? this.eventDatetime.toLocaleDateString(
        [],
        {
          dateStyle: "full"
        }
      )
      : "TBD"
    )
  },
  get eventTime() {
    return (
      this.eventDatetime
      ? this.eventDatetime.toLocaleTimeString(
          [],
          {hour: "numeric", minute: "2-digit"}
        )
      : "TBD"
    )
  },

  get location() {
    return this.data.value.location ?? "TBD"
  },
  get locationLink() {
    return this.data.value.locationLink ?? null
  },
  get address() {
    return this.data.value.address ?? null
  },
  get addressLink() {
    return this.data.value.addressLink ?? null
  },
  get googleCalendarLink() {
    return this.data.value.googleCalendarLink ?? null
  },
  get hasIcs() {
    return this.data.value.hasIcs ?? false
  },

  get latLon() {
    return this.data.value.latLon ?? null
  }
};

onBeforeMount(async () => {
  return fetch(
    "/api/get-copy/homepage",
    {
      credentials: "include"
    }
  )
  .then(response => response.json())
  .then(data => {
    homepageInfo.data.value = data;
    return data
  })
  .then(data => {
    if (data.latLon !== null) {
      const latLon = data.latLon.split(", ");
      const lat = Number(latLon[0]);
      const lon = Number(latLon[1]);

      let map = L.map('map').setView([lat, lon], 16);

      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);

      L.marker([lat, lon]).addTo(map)
      .bindTooltip("Steeplejack Brewing")
      .openTooltip();
    }
  })
})
</script>

<template>
  <main>
    <NavBar/>

    <div class="content">
      <div class="titles">
        <h1 class="title">{{ homepageInfo.title }}</h1>
        <p class="subtitle">{{ homepageInfo.subtitle }}</p>
      </div>

      <div class="calendar-links">
        <a
        v-if="homepageInfo.googleCalendarLink !== null"
        class="calendar-link"
        :href="homepageInfo.googleCalendarLink"
        target="_blank"
        rel="noopener noreferrer"
        >
          Add to Google Calendar
        </a>
        <a
        v-if="homepageInfo.hasIcs"
        href="/api/calendar/baby-shower.ics"
        download
        >
          Download iCal event
        </a>
      </div>

      <div class="info">
        <p>
          Please join us at {{ homepageInfo.eventTime }}
          on {{ homepageInfo.eventDate }} at
          <a :href="homepageInfo.locationLink">{{ homepageInfo.location }}</a>!
        </p>
        <p>
          <a :href="homepageInfo.addressLink">{{ homepageInfo.address }}</a>
        </p>
      </div>

      <div id="map" v-show="homepageInfo.latLon !== null"></div>

    </div>

  </main>
</template>

<style scoped>
main {
  grid-template-columns: 1fr;
  grid-template-rows: max-content 1fr;
  grid-template-areas:
    "nav"
    "content";
}

.content {
  display: grid;
  grid-template-rows: repeat(3, max-content) auto;
  grid-template-columns: auto;
  grid-auto-flow: column;
}

.subtitle {
  font-size: var(--h2-size);
}

.calendar-links {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-around;
  margin: 1em 0;
}
.calendar-links a {
  height: 100%;
  text-decoration: none;
  border: 1px solid var(--blue);
  padding: 0.5em;
}

nav {
  grid-area: nav;
}

.content {
  grid-area: content;
  width: max-content;
  max-width: 50vw;
  height: 100%;
  margin: 0 auto;
}

.title {
  font-size: 4rem;
  user-select: none;
  -webkit-user-select: none;
}

.info {
  grid-area: unset;
  display: flex;
  flex-direction: column;
  gap: 0.1em;
  padding: 1em 0;
  width: 100%;
}
.info p {
  margin: 0;
  width: 100%;
  max-width: unset;
}

.itinerary {
  width: 100%;
  font-size: var(--h2-size);
}
.itinerary td:first-of-type {
  text-align: right;
  padding-right: 0.5em;
}
.itinerary td:nth-of-type(2) {
  padding-left: 0.5em;
}

#map {
  height: 100%;
  min-height: 20rem;
  width: 100%;
}


@media (width < 800px) {
  .content {
    max-width: 90vw;
  }

  .title {
    font-size: var(--h1-size);
  }
}
</style>