$selected = { "power" => 0, "light" => "rgba(255, 0, 0, 0.7)", "mode" => "select" }
$view = { "size_x" => 10, "size_y" => 10,"fd" => 0
}

# $view의 monster는 random moviedex index

class PowerController < ApplicationController
  def on
    if $selected["power"] == 0

      $selected["power"] = 1
      $selected["light"] = "rgba(0, 128, 0, 0.7)"
      $selected["mode"] = "select"

      $player = {
        "hit" => 1,
        "hp" => 20,
        "pos" => [0, 0],
        "caught_movie_dex" => [],
        "current_moviedex" => 0,
        "movie_title" => "",
        "movie_poster" => "",
        "movie_year" => "",
        "movie_director" => "",
        "movie_writer" => "",
        "movie_rate" =>0,
        "movie_genre" => "",
        "pos_x" => 0,
        "pos_y" => 0
      }

      $game = {
        "movie_dex" => [],
        "monster" => 0,
        "monster_hp" => 0
      }

      File.readlines("movie_info.json").each do |line|
        $game["movie_dex"] << JSON.parse(line)
      end
    end
  end

  def off
    $selected["power"] = 0
    $selected["light"] = "rgba(255, 0, 0, 0.7)"
    $selected["mode"] = "map"
    $player = { "pos_x" => 0, "pos_y" => 0, "hp" => 0}
    $selected = { "power" => 0, "light" => "rgba(255, 0, 0, 0.7)", "mode" => "select" }
  end

end
