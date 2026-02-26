// main.typ
#import "theme.typ": *
#show: setup


// -- CONTENT
#title-slide(
  extra: {
    set align(center)
    stack(
      dir: ltr,
      spacing: 2cm,
      image("../architect_face.svg", height: 1.2cm),
    )
  }
)

== Sommaire

#components.adaptive-columns(outline(title: none, indent: 1em, depth: 1))


= Lorem
== Ma Super Grille

#matrix-slide(
  //title: [Ma Super Grille],
  subtitle: [Sous titre],
  conclusion: [*Note :* conclusion.],
  columns: (1fr, 2fr, 1fr),
  ..(lorem(8),) * 9
)

== Simple slide

Contenue simple

#matrix-slide(
  title: [Ma Super Grille], // Doublon ?
  subtitle: [Sous-titre de présentation],
  columns: 3,
  sections: (
    (title: "Bloc 1", content: lorem(10), color: blue),
    (title: "Bloc 2", content: lorem(15), color: blue.lighten(20%)),
    (title: "Bloc 3", content: lorem(10)),
    [Contenu sans titre direct],
  ),
  conclusion: [Note : Cette grille est maintenant fonctionnelle.]
)

#focus-slide("Merci")