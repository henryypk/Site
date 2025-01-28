document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".tipos");
  const items = document.querySelectorAll(".produtos");
  let activeFilter = null; // Para rastrear o filtro ativo

  buttons.forEach(button => {
    button.addEventListener("click", () => {
      const filter = button.getAttribute("data-filter");

      // Alternar o filtro ativo
      if (activeFilter === filter) {
        activeFilter = null; // Remover o filtro
        showAllItems(); // Mostrar todos os itens
      } else {
        activeFilter = filter; // Atualizar o filtro ativo
        filterItems(filter); // Filtrar itens
      }
    });
  });

  // Filtra os itens com a categoria selecionada
  function filterItems(filter) {
    items.forEach(item => {
      if (item.classList.contains(filter)) {
        fadeIn(item); // Se o item tiver a categoria, mostre-o
      } else {
        fadeOut(item); // Caso contrário, esconda
      }
    });
  }

  // Mostra todos os itens
  function showAllItems() {
    items.forEach(item => fadeIn(item)); // Mostra todos os itens
  }

  function fadeIn(element) {
    element.style.display = "flex"; // Garante que o item seja exibido como flex
    setTimeout(() => {
      element.style.transition = "opacity 0.5s ease";
      element.style.opacity = "1"; // Aumenta a opacidade
    }, 0);
  }

  function fadeOut(element) {
    element.style.transition = "opacity 0.5s ease";
    element.style.opacity = "0"; // Diminuir a opacidade
    setTimeout(() => {
      element.style.display = "none"; // Esconde após o fade
    }, 500); // Tempo igual ao do fade (0.5s)
  }

});

const carousel = new bootstrap.Carousel('#myCarousel')

function butao() {
  alert('Compra realizada com sucesso!');
}

// document.addEventListener("DOMContentLoaded", () => {
//   console.log('oi');
//   const buttons = document.querySelectorAll(".tipos");
//   const items = document.querySelectorAll(".produtos");
//   let activeFilter = null; // Para rastrear o filtro ativo

//   // Quando um botão de filtro for clicado, alterna entre os filtros
//   buttons.forEach(button => {
//     button.addEventListener("click", () => {
//       const filter = button.getAttribute("data-filter");
//       console.log('oi');

//       // Alternar o filtro ativo
//       if (activeFilter === filter) {
//         activeFilter = null; // Remover o filtro
//         showAllItems(); // Mostrar todos os itens
//       } else {
//         activeFilter = filter; // Atualizar o filtro ativo
//         filterItems(filter); // Filtrar itens
//       }
//     });
//   });

//   // Filtra os itens com a categoria selecionada
//   function filterItems(filter) {
//     items.forEach(item => {
//       if (item.classList.contains(filter)) {
//         fadeIn(item); // Se o item tiver a categoria, mostre-o
//       } else {
//         fadeOut(item); // Caso contrário, esconda
//       }
//     });
//   }

//   // Mostra todos os itens
//   function showAllItems() {
//     items.forEach(item => fadeIn(item)); // Mostra todos os itens
//   }

//   // Função para aplicar fade-out (esconder)
//   function fadeOut(element) {
//     element.style.transition = "opacity 0.5s ease";
//     element.style.opacity = "0"; // Diminuir a opacidade
//     setTimeout(() => {
//       element.style.display = "none"; // Esconde após o fade
//     }, 500); // Tempo igual ao do fade (0.5s)
//   }

//   // Função para aplicar fade-in (mostrar)
//   function fadeIn(element) {
//     element.style.display = "flex"; // Garante que o item seja exibido como flex
//     setTimeout(() => {
//       element.style.transition = "opacity 0.5s ease";
//       element.style.opacity = "1"; // Aumenta a opacidade
//     }, 0);
//   }
// });

