// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MyNFT {
    string public name = "MyNFT"; // Название коллекции
    string public symbol = "MNFT"; // Символ коллекции
    uint256 public tokenCounter; // Счетчик созданных токенок

    mapping(uint256 => address) public ownerOf; // Владелец каждого токена по ID
    mapping(address => uint256) public balanceOf; // Количество NFT у адреса
    mapping(uint256 => string) public tokenURI; // URI метаданных каждого токена

    // Событие, стандартное для ERC-721
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);

    // Создание нового NFT
    function mint(string memory _uri) public returns (uint256) {
        uint256 newTokenId = tokenCounter; // ID нового токена
        ownerOf[newTokenId] = msg.sender; // владельцем становится вызывающий
        balanceOf[msg.sender] += 1; // увеличение баланса
        tokenURI[newTokenId] = _uri; // сохранение URI
        tokenCounter += 1; // увеличение счетчика
        emit Transfer(address(0), msg.sender, newTokenId); // mint - событие создания
        return newTokenId;
    }
}
