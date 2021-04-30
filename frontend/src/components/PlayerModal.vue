<template>
  <div v-if="selected" class="personalResultsModal">
    <h1 class="code">
      {{ selected_player.name }}
    </h1>
    <p class="date">
      {{ date }}
    </p>
    <div class="hr" />
    <h3 class="title">
      Individual results
    </h3>
    <div
      class="close-button"
      @click="deselectPlayer()"
    >
      <div
        id="line1"
        class="line"
      />
      <div
        id="line2"
        class="line"
      />
    </div>
    <div
      class="personal-list"
    >
      <div
        v-for="guess in selected_player.guesses"
        :key="guess"
      >
        <GuessIcon
          :trackid="guess.info"
          :guess="guess.guess"
          :answer="guess.correct_answer"
        />
      </div>
    </div>
  </div>
</template>

