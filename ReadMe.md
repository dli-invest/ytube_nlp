### Annotate Youtube Videos

To run subdirectory scripts use

```
python -m lib.youtube.yt_nlp -v VuavFEzN6oA
```

Note the cron jobs are 24 hours delayed in order to get transcripts.

#### Tasks

- [ ] Text summarization
- [ ] Back to home button
- [ ] Sentiment analysis average for video
- [ ] More nlp options
- [ ] Update Page titles
- [ ] Improving searching - index pages per channel? Or filters per channel name?

**02/20/2021**

- [x] adding icecream
- [x] fixing links

Since youtube seems to get transcripts for every video now, I can start adding more videos to scan.

Think about analyzing wall street reporter videos for sentiment analysis.

**09/02/2020**
- [x] Fixed issues with sending new data needed `to_dict('records')` instead of `to_dict()`
- [x] Improved index.html file

**08/30/2020**
- [x] Added new super stock wall street reporter to youtube nlp

**07/21/2020**
- [x] update nlp logic on match for (ar, blockchain)

**07/04/2020**
- [x] Logic to handle youtube channels without subtitles (just parse title and description)
- [x] Logic to nlp just titles and descriptions
- [x] Email Notifications or something (setup notification on golang server?)
- [x] Discord Notifications for key topics (ar, blockchain) (not doing)

**07/03/2020**
- [x] Applied API key to github secrets
- [x] Added Basic Orphaned gh-pages branch using `git checkout --orphan gh-pages`
- [x] Basic Glue Logic
- [x] Discovered Unpopular channels are missing annotations

**07/02/2020**

- [x] Basic spacy annotation
- [x] Basic Report Generation
- [x] Github Actions Configured
