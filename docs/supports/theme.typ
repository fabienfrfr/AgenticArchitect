// theme.typ
#import "@preview/touying:0.5.3": *
#import themes.metropolis: *

#let blue = rgb("#0055A4")

#let setup(body) = {
  show: metropolis-theme.with(
    aspect-ratio: "16-9",
    footer: context {
      if counter(page).get().first() > 1 { // > 1 pour éviter le footer sur la page de titre
        block(width: 100%, inset: (x: 1.0cm, bottom: 0.025cm))[
          #grid(
            columns: (1fr, auto, 1fr),
            align(left, image("../architect_face.svg", height: 0.3cm)),
            align(center, text(size: 8pt, fill: gray)[Confidential C1 - Fabien Furfaro - 2026])
          )
        ]
      }
    },
    config-colors(
      primary: blue,
      primary-dark: blue.darken(10%),
      secondary: blue.lighten(20%),
      accent: blue,
    ),
    config-common(margin: (bottom: 2cm)),
    config-info(
      title: [Titre du Projet],
      subtitle: [Documentation de L'Architecte],
      author: [Fabien FURFARO],
    ),
  )
  body
}

#let matrix-slide(
  title: none,
  subtitle: none,
  conclusion: none,
  columns: none,
  gutter: 12.5pt,
  text-size: 11.5pt,
  header-radius: 5pt,
  sections: (),
  ..args
) = {
  let all_sections = sections + args.pos()
  slide[
    #if title != none { [== #title] }
    #if subtitle != none {
      v(-0.5em)
      block(inset: (bottom: 15pt, left: 2pt))[#text(0.9em, fill: gray.darken(40%))[#subtitle]]
    }

    #set text(size: text-size)
    #let n = all_sections.len()
    #let cols = if columns != none { 
      if type(columns) == int { (1fr,) * columns } else { columns } 
    } else { (1fr,) * calc.min(n, 3) }

    #grid(
      columns: cols,
      column-gutter: gutter,
      row-gutter: gutter,
      ..all_sections.map(s => {
        let is_dict = type(s) == dictionary
        let s_title = if is_dict { s.at("title", default: none) } else { none }
        let s_cont = if is_dict { s.at("content", default: []) } else { s }
        let s_col = if is_dict { s.at("color", default: blue) } else { blue }

        stack(spacing: 8pt,
          if s_title != none {
            block(fill: s_col, width: 100%, inset: 6pt, radius: header-radius)[
              #align(center, text(fill: white, weight: "bold", s_title))
            ]
          },
          s_cont
        )
      })
    )

    #if conclusion != none {
      v(1fr)
      block(width: 100%, inset: (top: 8pt), stroke: (top: 0.5pt + gray))[
        #set text(fill: gray.darken(20%), style: "italic")
        #conclusion
      ]
    }
  ]
}