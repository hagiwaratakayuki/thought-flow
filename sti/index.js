const fs = require("node:fs");

const StreamObject = require('stream-json/streamers/StreamObject');
const stream = fs.createReadStream("./bulkdata/ntrs-public-metadata.json", { encoding: "utf-8" });
const results = [];
let index = 0;
let start = new Date()
let st = stream.pipe(StreamObject.withParser()).on('data', function (data) {
    index += 1;
    /*
    if (index % 1000 === 0) {
        console.log(index);
    }*/
    if (index % 10000 === 0) {
        const now = new Date()
        console.log((now - start.getTime()) / 1000)
        start = now;
    }
    if (index < 100000) {
        return
    }

    if (results.length >= 2000) {
        st.pause();
    }
    try {
        const value = data.value;

        if (!value.authorAffiliations) {
            return;
        }
        const title = value.title;
        const body = value.abstract;
        const id = value.id;

        const publicationDates = value.publications.filter(function (r) {
            return r.publicationDate.indexOf('19') == 0 || r.publicationDate.indexOf('20') == 0;

        })

        if (publicationDates.length === 0) {
            return

        }

        const published = publicationDates[0].publicationDate;

        const author = value.authorAffiliations[0]?.meta?.author?.name;

        const orcId = value.authorAffiliations[0]?.meta?.author?.orcid;
        const stiId = value.authorAffiliations[0]?.id;

        const authorid = orcId || stiId || '';
        const result = {
            id,
            title,
            body,
            author,
            authorid,
            published

        }
        results.push(result)
    } catch (error) {
        console.dir(error);
        st.pause();
    }




}).on("end", function () {
    console.log('end');

    console.log(results.length);

}).on("pause", function () {
    const res = JSON.stringify(results)
    fs.writeFile("./bulkdata/parsed.json", res, { encoding: "utf-8" }, function (...args) {
        console.dir(args);
        console.log('done!');
    })
});
