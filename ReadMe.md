### Annotate Youtube Videos

To run subdirectory scripts use

```
python -m lib.yt_nlp -v VuavFEzN6oA
```

#### Tasks

Think about analyzing wall street reporter videos for sentiment analysis.

**08/30/2020**
- [] Added new super stock wall street reporter to youtube nlp

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
