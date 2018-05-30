# Website Scrape-And-Deploy

The goal of this script is to scrape all files of your website which you host locally. Then, you can use the AWS CLI to upload your static files to a S3 bucket. 

## Configuration

Rename `scrapy.cfg.example` to `scrapy.cfg`.

## Execute

First crawl all the pages:

```
scrapy crawl web -a root_url=https://www.data-blogger.com/ -a output_path=/media/sf_Ubuntu/website-scrape-and-deploy/output/ -a exclude=/oembed/
```

Here, I specified the root URL. The `sitemap.xml`, `robots.txt` and `index.html` are automatically crawled. You need to specify where you want to store the output and you can optionally specify which URLs you would like to exclude (here: URLs containing `/oembed/`).

Then, you should upload your crawled files to a AWS S3 static website bucket:

```
aws s3 cp /media/sf_Ubuntu/website-scrape-and-deploy/output/ s3://www.data-blogger.com --recursive
```

And last but not least, you can invalidate any CloudFront cache:

```
aws cloudfront create-invalidation --distribution-id EQNYJUCRR9HHL --paths /*
```

In summary, the following one-liner can be used for generating the static website pages and upload it to AWS s3:

```
scrapy crawl web -a root_url=https://www.data-blogger.com/ -a output_path=/media/sf_Ubuntu/website-scrape-and-deploy/output/ -a exclude=/oembed/ && aws s3 cp /media/sf_Ubuntu/website-scrape-and-deploy/output/ s3://www.data-blogger.com --recursive && aws cloudfront create-invalidation --distribution-id EQNYJUCRR9HHL --paths /*
```