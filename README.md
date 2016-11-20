## Inspiration

Google Knowledge graph is a powerful semantic web API that allows web scrapers to collect structured and machine readable data from unstructured data on the web, and it enables intelligent assistants like Google Now to answer questions about knowledge in a natural way. However, things like Google KG are rarely aware of specific knowledge about college campuses. They know when flights are coming, but not when your school bus is coming. Our chatbot aimed to assist students on discovering information on their campus via a simple messenger interface. It also allows students to share events to the campus community in a trusted environment.

## What it does

FaceBook messenger bot that allows users to seek information about Duke University campus, such as restaurants, events, and bus schedules.

## How we built it

- Python back-end with Flask framework
- Google App Engine with Cloud Datastore for hosting and database management
- Wit.AI for natural language processing
- BeautifulSoup web scraper to scrape Duke restaurant information off campus website
- TransLoc API to scrape current bus locations and calculate expected arrival time

## Team

Paris Morgan - Duke
Walter Huang - Case
Adam Tache - Duke
