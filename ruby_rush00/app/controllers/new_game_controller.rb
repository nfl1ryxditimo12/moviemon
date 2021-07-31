class NewGameController < ApplicationController
  def game
    $selected["mode"] = "game"
    $player["hp"] = 20
    if params[:input] == "u"
      if $player["pos_y"] - 9 >= 0
        $player["pos_y"] -= 9
        if Random.new.rand(100) > 85
          $selected["mode"] = "fight"
          $game["monster"] = rand(40)
          $game["monster_hp"] = (($game["movie_dex"][$game["monster"]]["Ratings"]).to_i) + 10
          #전체 무비덱스에서 해당 포켓몬 삭제t\
          redirect_to "/fight"
        else
          redirect_back fallback_location: 'game'
          #redirect_to "/game"
        end
      end
    elsif params[:input] == "d"
      if $player["pos_y"] + 9 < 90
        $player["pos_y"] += 9
        if Random.new.rand(100) > 85
          $selected["mode"] = "fight"
          $game["monster"] = rand(40)
          $game["monster_hp"] = (($game["movie_dex"][$game["monster"]]["Ratings"]).to_i) + 10
          #전체 무비덱스에서 해당 포켓몬 삭제t\
          redirect_to "/fight"
        else
          redirect_back fallback_location: 'game'
          #redirect_to "/game"
        end
      end
    elsif params[:input] == "l"
      if $player["pos_x"] - 10 >= 0
        $player["pos_x"] -= 10
        if Random.new.rand(100) > 85
          $selected["mode"] = "fight"
          $game["monster"] = rand(40)
          $game["monster_hp"] = (($game["movie_dex"][$game["monster"]]["Ratings"]).to_i) + 10
          #전체 무비덱스에서 해당 포켓몬 삭제t\
          redirect_to "/fight"
        else
          redirect_back fallback_location: 'game'
          #redirect_to "/game"
        end
      end
    elsif params[:input] == "r"
      if $player["pos_x"] + 10 < 100
        $player["pos_x"] += 10
        if Random.new.rand(100) > 85
          $selected["mode"] = "fight"
          $game["monster"] = rand(40)
          $game["monster_hp"] = (($game["movie_dex"][$game["monster"]]["Ratings"]).to_i) + 10
          #전체 무비덱스에서 해당 포켓몬 삭제t\
          redirect_to "/fight"
        else
          redirect_back fallback_location: 'game'
          #redirect_to "/game"
        end
      end
    end
  end

  def load
    $selected["mode"] = "select"
    if params[:input] == "d"
      $view["fd"]  += 1
      redirect_back fallback_location: '/'
    elsif params[:input] == "u"
      $view["fd"] -=1
      redirect_back fallback_location: '/'
    end
    $view["fd"] += 3
    $view["fd"] %= 3
  end

  def fight

    if params[:input] == nil
      $selected["mode"] = "fight"
    end

    if params[:input] == "fight"

      if $game["monster_hp"] - $player["hit"] <= 0
        $game["monster_hp"] = 0;
        $selected["mode"] = "win"
        $player["hp"] = 20
        $player["hit"] += 1
        $player["caught_movie_dex"] << $game["monster"]
      elsif $player["hp"] - 1 <= 0 && $selecte["mode"] != "win"
        $selected["mode"] = "lose"
        $player["hp"] = 0
      else
        $game["monster_hp"] -= $player["hit"]
        $player["hp"] -= 1
        redirect_back fallback_location: 'game'
      end

    elsif params[:input] == "run"
      $selected["mode"] = "run"
    end

    if $selected["mode"] != "win" && $player["hp"] - 1 <= 0
      $player["hp"] = 0
      $selected["mode"] = "lose"
    end
  end

end
