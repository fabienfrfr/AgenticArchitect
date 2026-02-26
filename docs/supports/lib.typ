#let project_style(
  title: "",
  subtitle: "Documentation",
  authors: (),
  body
) = {
  // --- CONFIGURATION GLOBALE ---
  set text(lang: "fr", size: 11pt, font: "New Computer Modern")
  set page(
    paper: "a4",
    margin: (x: 2.5cm, y: 3cm),
    numbering: "1",
    header: context {
      if counter(page).get().first() > 1 {
        grid(
          columns: (1fr, 1fr),
          text(9pt, gray)[#title],
          align(right, text(10pt, gray)[#counter(page).display()])
        )
      }
    }
  )
  set heading(numbering: "1.1.")
  set par(justify: true, leading: 0.65em)

  let blue_1 = rgb("#002a54")
  let blue_2 = rgb("#0070ad")

  // --- PAGE DE GARDE ---
  align(center)[
    #grid(
      columns: (1fr, 1fr),
      align(left, image("../architect_face.svg", width: 40%)),
      align(right, image("../architect_face.svg", width: 40%))
    )
    
    #v(5cm)
    #text(26pt, weight: "bold", fill: blue_1)[#title] \
    #v(1em)
    #text(16pt, style: "italic", gray)[#subtitle] \
    #v(1cm)
    #line(length: 80%, stroke: 1.5pt + blue_2)
    
    #v(4cm)
    #grid(
      columns: (1fr, 1fr),
      align(left)[
        *Auteurs :* \
        #authors.join([\ \ ])
      ],
      align(right)[
        *Organisation :* \
        TheArchitect \
        *Date :* #datetime.today().display("[month] [year]")
      ]
    )
  ]

  pagebreak()
  
  // --- TABLE DES MATIÈRES ---
  outline(indent: auto)
  pagebreak()

  body
}

#let infobox(content) = {
  let blue_2 = rgb("#0070ad")
  block(
    fill: blue_2.lighten(95%),
    inset: 12pt,
    radius: 4pt,
    stroke: (left: 4pt + blue_2),
    width: 100%,
    content
  )
}