import { instantMeiliSearch } from "@meilisearch/instant-meilisearch";

const search = instantsearch({
  indexName: "lister",
  searchClient: instantMeiliSearch(
    "<URL",
    "<SEARCH_KEY>",
    {
      limitPerRequest: 30
    }
  )
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: "#searchbox"
  }),
  instantsearch.widgets.clearRefinements({
    container: "#clear-refinements"
  }),
  instantsearch.widgets.refinementList({
    container: "#year-list",
    attribute: "year",
    limit: 5, 
    showMore: true
  }),
  instantsearch.widgets.refinementList({
    container: "#credit-list",
    attribute: "credit"
  }),
  instantsearch.widgets.refinementList({
    container: "#type-list",
    attribute: "type"
  }),
  instantsearch.widgets.configure({
    hitsPerPage: 5,
   // snippetEllipsisText: "...",
   // attributesToSnippet: ["description:50"]
  }),
  instantsearch.widgets.hits({
    container: "#hits",
    templates: {
      item: `
        <div>
          <div class="hit-name">
            {{#helpers.highlight}}{ "attribute": "date" }{{/helpers.highlight}}
          </div>
          <div class="hit-description">
            {{#helpers.snippet}}{ "attribute": "entry" }{{/helpers.snippet}}
          </div>
          <div class="hit-info">Transcript: <a href="{{transcript}}" target="_blank">{{transcript}}</a></div>
          <div class="hit-info">Transcription credit: {{credit}}</div>
        </div>
      `
    }
  }),
  instantsearch.widgets.pagination({
    container: "#pagination",
    showLast: false
  })
]);

search.start();

