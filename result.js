document.getElementById('queryForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const query = document.getElementById('query').value;
    const rows = document.getElementById('rows').value;

    const minYear = parseInt(document.getElementById('minYear').value, 10);
    const maxYear = parseInt(document.getElementById('maxYear').value, 10);

    const params = {
        q: query,
        q_op: "AND",
        start: 0,
        rows: parseInt(rows, 10),
        defType: "edismax",
        qf: "Description^5 Participants^4 Country^3 Name_War^2 Winner"
    };

    try {
        const response = await axios.post("http://127.0.0.1:5000/query-solr", {
            uri: "http://localhost:8983/solr", 
            collection: "wikiwar",           
            params: params                    
        });

        const resultsDiv = document.getElementById('queryResults');
        resultsDiv.innerHTML = ""; 

        const docs = response.data.response.docs;

        docs.forEach(doc => {
            const title = "Battle of " + doc.ID;
            const description = doc.Description || 'No description available.';
            const year = doc.Year;

            if (year < minYear || year > maxYear) {
                return; 
            }

            const resultDiv = document.createElement('div');
            resultDiv.classList.add('result');

            resultDiv.innerHTML = `
                <h2 class="battle-title">${title}</h2>
                <p class="battle-description">${description}</p>
                <p class="battle-year">Year: ${year}</p>
                <a href="http://127.0.0.1:5000/battle-detail/${doc.ID}" class="see-more-btn">See more details..</a>
            `;

            resultsDiv.appendChild(resultDiv);
        });

    } catch (error) {
        console.error("Error fetching Solr results: ", error);
        alert("Failed to fetch results from Solr. Please try again later.");
    }
});
