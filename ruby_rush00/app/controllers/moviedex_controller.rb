class MoviedexController < ApplicationController
  def index
    @position = params[:btn]

    if @position == 'r'
      $player["current_moviedex"] < $player["caught_movie_dex"].length - 1 ? $player["current_moviedex"] += 1 : $player["current_moviedex"] = 0
    elsif @position == 'l'
      $player["current_moviedex"] > 0 ? $player["current_moviedex"] -= 1 : $player["current_moviedex"] = $player["caught_movie_dex"].length - 1
    end
    
    $player["movie_title"] = $game["movie_dex"][$player["caught_movie_dex"][$player["current_moviedex"]]]["Title"]
    $player["movie_year"] = $game["movie_dex"][$player["caught_movie_dex"][$player["current_moviedex"]]]["Year"]
    $player["movie_genre"] = $game["movie_dex"][$player["caught_movie_dex"][$player["current_moviedex"]]]["Genre"]
    $player["movie_director"] = $game["movie_dex"][$player["caught_movie_dex"][$player["current_moviedex"]]]["Director"]
    $player["movie_writer"] = $game["movie_dex"][$player["caught_movie_dex"][$player["current_moviedex"]]]["Writer"]
    $player["movie_plot"] = $game["movie_dex"][$player["caught_movie_dex"][$player["current_moviedex"]]]["Plot"]
    $player["movie_poster"] = $game["movie_dex"][$player["caught_movie_dex"][$player["current_moviedex"]]]["Poster"]
    $player["movie_rate"] = $game["movie_dex"][$player["caught_movie_dex"][$player["current_moviedex"]]]["Ratings"]

  end
end
