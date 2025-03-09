<script setup>
import { onBeforeMount } from "vue";
import NavBar from "../components/NavBar.vue";
import { ref } from "vue";
import { useMouseImage } from "@/composables/mouseImage";

useMouseImage("/images/dancing-baby.gif");

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
      return new Date(Date.parse(this.data.value.datetime))
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
})
</script>

<template>
  <main>
    <NavBar :dark-bg="true"/>

    <div class="content">
      <div class="titles">
        <div>
          <h1 class="title">{{ homepageInfo.title }}</h1>
          <p class="subtitle">{{ homepageInfo.subtitle }}</p>
        </div>
      </div>

      <div class="itinerary">
        <div>
          <p>
            Please join us at {{ homepageInfo.eventTime }}
            on {{ homepageInfo.eventDate }} at
            <a
            :href="homepageInfo.locationLink" 
            target="_blank"
            rel="noopener noreferrer"
            >{{ homepageInfo.location }}</a>!
          </p>
          <p>
            <a
            :href="homepageInfo.addressLink"
            target="_blank"
            rel="noopener noreferrer"
            >{{ homepageInfo.address }}</a>
          </p>
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
      </div>

    </div>

  </main>
</template>

<style scoped>
main {
  background-image: url(/images/homepage-background.jpg);
  background-position: center;
  background-size: cover;
}

main {
  grid-template-columns: 1fr;
  grid-template-rows: max-content 1fr;
  grid-template-areas:
    "nav"
    "content";
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

  display: grid;
  grid-template-rows: auto repeat(1, max-content);
  grid-template-columns: auto;
  grid-template-areas:
  "titles"
  "info";
  gap: 0.5rem
}

.titles {
  grid-area: titles;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.titles div,
.itinerary {
  background-color: color-mix(in srgb, var(--color-bg) 60%, transparent);
  backdrop-filter: blur(3px);
  padding: 1em;
}

.title {
  font-size: 4rem;
  user-select: none;
  -webkit-user-select: none;
}

.subtitle {
  font-size: var(--h2-size);
}
.title,
.subtitle {
  width: 100%;
  text-align: center;
}

.calendar-links {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.125em;
  flex-shrink: 1;
  width: max-content;
}
.calendar-links a {
  text-decoration: none;
  background-color: var(--blue);
  color: var(--color-bg);
  padding: 0.25em;
  width: 100%;
  font-size: var(--base-font-size);
}
.calendar-links a:hover {
  background-color: var(--blue-2);
}

.itinerary {
  grid-area: info;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0.4em;
  width: 100%;
  font-size: var(--h3-size);
}
.itinerary div:first-child{
  flex-grow: 1;
}
.itinerary p {
  margin: 0;
  width: 100%;
  max-width: unset;
}

@media (width < 800px) {
  main {
    background-image: url(/images/homepage-background-mobile.jpg);
  }
  .content {
    max-width: 90vw;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .title {
    font-size: var(--h1-size);
  }
  .subtitle {
    font-size: inherit;
  }

  .itinerary {
    flex-direction: column;
  }

  .calendar-links,
  .calendar-links a {
    width: 100%;
  }
}
</style>