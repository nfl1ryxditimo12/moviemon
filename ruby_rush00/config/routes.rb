Rails.application.routes.draw do
  
  # 전원 관리
  get '/' => "power#off"
  get '/off' => "power#off"
  get '/on' => "power#on"
  
  # 게임 시작, 로드
  get "/game" => "new_game#game"
  get "/load" => "new_game#load"
  get '/fight' => "new_game#fight"

  # on game
  # get "/game/:input" => "new_game#move"

  # World map
  get "/world" => "map#world"

  #movie index
  get '/moviedex' => 'moviedex#index'

  #file_manage
  get 'read' => 'fm#read'
  get 'save' => 'fm#save'
end
