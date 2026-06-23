function decision(score){

    if(score >= 0.75){
        return ["Strong Hire","strong"];
    }

    if(score >= 0.72){
        return ["Hire","hire"];
    }

    return ["Consider","consider"];
}

/* =========================
   Animated Score
========================= */

function animateScore(element,target){

    let current = 0;

    const duration = 800;
    const frameRate = 16;

    const increment =
    target / (duration/frameRate);

    const timer = setInterval(()=>{

        current += increment;

        if(current >= target){

            current = target;
            clearInterval(timer);

        }

        element.innerHTML =
        current.toFixed(3);

    },frameRate);
}

/* =========================
   Render Candidate Table
========================= */

function renderTable(data){

    const table =
    document.getElementById(
        "candidateTable"
    );

    table.innerHTML = "";

    data.forEach(c=>{

        const d =
        decision(c.score);

        table.innerHTML += `

        <tr onclick="showCandidate('${c.candidate_id}')">

            <td>${c.rank}</td>

            <td>${c.candidate_id}</td>

            <td>${Number(c.score).toFixed(3)}</td>

            <td>

                <span class="badge ${d[1]}">
                    ${d[0]}
                </span>

            </td>

        </tr>

        `;

    });

}

/* =========================
   Candidate Intelligence
========================= */

function showCandidate(id){

    const c =
    candidates.find(
        x => x.candidate_id === id
    );

    const d =
    decision(c.score);

    document.getElementById(
        "candidateDetails"
    ).innerHTML = `

    <div class="candidate-card">

        <h3>
            ${c.candidate_id}
        </h3>

        <h1
            id="animatedScore"
            class="candidate-score"
        >
            0.000
        </h1>

        <div class="candidate-rank">

            Rank #${c.rank}

        </div>

        <div class="rank-explanation">

            <h4>Ranking Factors</h4>

            <ul>

                <li>Semantic Similarity Score</li>

                <li>Behavioral Signals</li>

                <li>Recruiter Response Rate</li>

                <li>Interview Completion Rate</li>

                <li>Technical Skill Alignment</li>

            </ul>

        </div>

        <br>

        <span class="badge ${d[1]}">

            ${d[0]}

        </span>

        <br><br>

        <div class="candidate-reason">

            <h3>Why This Candidate?</h3>

            <br>

            ✓ Strong semantic alignment with job requirements

            <br><br>

            ✓ Relevant retrieval, ranking and AI expertise

            <br><br>

            ✓ High recruiter engagement indicators

            <br><br>

            ✓ Strong vector search and embedding knowledge

            <br><br>

            ✓ Consistently high overall ranking score

            <br><br>

            <strong>Recruiter Explanation:</strong>

            <br><br>

            ${c.reasoning}

        </div>

    </div>

    `;

    animateScore(
        document.getElementById(
            "animatedScore"
        ),
        Number(c.score)
    );

}

/* =========================
   Search
========================= */

document
.getElementById(
    "searchBox"
)
.addEventListener(
    "keyup",
    e=>{

        const q =
        e.target.value
        .toLowerCase();

        const filtered =
        candidates.filter(
            c=>
            c.candidate_id
            .toLowerCase()
            .includes(q)
        );

        renderTable(filtered);

    }
);

/* =========================
   Initial Load
========================= */

window.addEventListener(
    "load",
    ()=>{

        renderTable(
            candidates
        );

        if(
            candidates &&
            candidates.length > 0
        ){

            showCandidate(
                candidates[0]
                .candidate_id
            );

        }

    }
);