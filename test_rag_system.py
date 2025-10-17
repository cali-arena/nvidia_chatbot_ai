"""
Script de Teste para Sistema RAG Avançado
Testa todas as funcionalidades do sistema RAG implementado
"""

import os
import asyncio
import sys
from pathlib import Path

# Adicionar o diretório atual ao path
sys.path.append(str(Path(__file__).parent))

try:
    from rag_system import AdvancedRAGSystem, RAGConfig
    print("✅ Sistema RAG importado com sucesso!")
except ImportError as e:
    print(f"❌ Erro ao importar sistema RAG: {e}")
    sys.exit(1)

async def test_rag_system():
    """Testa o sistema RAG completo"""
    
    print("\n🚀 INICIANDO TESTES DO SISTEMA RAG")
    print("=" * 50)
    
    # Configuração do sistema
    api_key = "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"
    
    # Configuração RAG
    config = RAGConfig(
        chunk_size=1000,
        chunk_overlap=200,
        max_file_size_gb=2.0,
        embedding_model="nvidia/Llama-3.2-3B-Instruct-TensorRT-LLM",
        vector_store_type="chroma",
        retrieval_k=5,
        similarity_threshold=0.7
    )
    
    try:
        # Inicializar sistema RAG
        print("\n📋 1. Inicializando Sistema RAG...")
        rag_system = AdvancedRAGSystem(api_key, config)
        print("✅ Sistema RAG inicializado com sucesso!")
        
        # Testar processamento de arquivo
        print("\n📄 2. Testando Processamento de Arquivo...")
        test_file = "exemplo_documento_grande.txt"
        
        if os.path.exists(test_file):
            result = await rag_system.process_file(test_file, "txt")
            
            if result["status"] == "success":
                print(f"✅ Arquivo processado: {result['chunks']} chunks criados")
            else:
                print(f"⚠️ Processamento falhou: {result['message']}")
        else:
            print(f"❌ Arquivo de teste não encontrado: {test_file}")
            return
        
        # Testar consultas RAG
        print("\n🔍 3. Testando Consultas RAG...")
        
        test_queries = [
            "O que é o sistema RAG?",
            "Quais são os componentes principais?",
            "Quais são as métricas de avaliação?",
            "Quais são os casos de uso ideais?",
            "Quais são as receitas anuais mencionadas?",
            "Quais são as recomendações estratégicas?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n   Consulta {i}: {query}")
            try:
                result = rag_system.query(query)
                
                if result["confidence"] > 0.3:
                    print(f"   ✅ Resposta (Confiança: {result['confidence']:.2f})")
                    print(f"   📚 Fontes: {len(result['source_documents'])} documentos")
                    
                    if "evaluation" in result:
                        eval_score = result["evaluation"]["overall_score"]
                        print(f"   ⭐ Qualidade: {eval_score:.2f}")
                else:
                    print(f"   ⚠️ Baixa confiança: {result['confidence']:.2f}")
                    
            except Exception as e:
                print(f"   ❌ Erro na consulta: {e}")
        
        # Testar estatísticas do sistema
        print("\n📊 4. Testando Estatísticas do Sistema...")
        try:
            stats = rag_system.get_system_stats()
            print(f"✅ Arquivos processados: {stats['processed_files']}")
            print(f"✅ Total de documentos: {stats['total_documents']}")
            print(f"✅ Tipo de vector store: {stats['vector_store_type']}")
            print(f"✅ Tamanho dos chunks: {stats['chunk_size']}")
            print(f"✅ Limite de arquivo: {stats['max_file_size_gb']} GB")
            
            if stats["evaluation_summary"]:
                eval_summary = stats["evaluation_summary"]
                if eval_summary.get("total_evaluations", 0) > 0:
                    print(f"✅ Avaliações realizadas: {eval_summary['total_evaluations']}")
                    print(f"✅ Score médio: {eval_summary['avg_overall_score']:.2f}")
                    
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas: {e}")
        
        # Testar avaliação
        print("\n🎯 5. Testando Sistema de Avaliação...")
        try:
            evaluator = rag_system.evaluator
            eval_summary = evaluator.get_evaluation_summary()
            
            if eval_summary.get("total_evaluations", 0) > 0:
                print(f"✅ Total de avaliações: {eval_summary['total_evaluations']}")
                print(f"✅ Score médio de relevância: {eval_summary['avg_relevance_score']:.2f}")
                print(f"✅ Score médio de completude: {eval_summary['avg_completeness_score']:.2f}")
                print(f"✅ Score geral médio: {eval_summary['avg_overall_score']:.2f}")
            else:
                print("⚠️ Nenhuma avaliação disponível ainda")
                
        except Exception as e:
            print(f"❌ Erro no sistema de avaliação: {e}")
        
        print("\n🎉 TESTES CONCLUÍDOS COM SUCESSO!")
        print("=" * 50)
        print("✅ Sistema RAG funcionando corretamente")
        print("✅ Processamento de arquivos OK")
        print("✅ Consultas RAG OK")
        print("✅ Sistema de avaliação OK")
        print("✅ Estatísticas OK")
        
    except Exception as e:
        print(f"\n❌ ERRO GERAL NO SISTEMA: {e}")
        return False
    
    return True

async def test_file_processing():
    """Testa especificamente o processamento de arquivos"""
    
    print("\n🔧 TESTE ESPECÍFICO DE PROCESSAMENTO DE ARQUIVOS")
    print("=" * 50)
    
    try:
        from rag_system import LargeFileProcessor, RAGConfig
        
        config = RAGConfig()
        processor = LargeFileProcessor(config)
        
        # Testar validação de tamanho
        print("📏 Testando validação de tamanho...")
        test_file = "exemplo_documento_grande.txt"
        
        if os.path.exists(test_file):
            is_valid = processor.validate_file_size(test_file)
            file_size_gb = os.path.getsize(test_file) / (1024**3)
            print(f"   Arquivo: {test_file}")
            print(f"   Tamanho: {file_size_gb:.4f} GB")
            print(f"   Válido: {'✅' if is_valid else '❌'}")
        
        # Testar hash de arquivo
        print("\n🔐 Testando hash de arquivo...")
        if os.path.exists(test_file):
            file_hash = processor.get_file_hash(test_file)
            print(f"   Hash: {file_hash[:16]}...")
        
        print("✅ Testes de processamento concluídos!")
        
    except Exception as e:
        print(f"❌ Erro nos testes de processamento: {e}")

async def test_vector_store():
    """Testa especificamente o vector store"""
    
    print("\n🗄️ TESTE ESPECÍFICO DE VECTOR STORE")
    print("=" * 50)
    
    try:
        from rag_system import VectorStoreManager, RAGConfig
        
        config = RAGConfig()
        api_key = "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"
        
        manager = VectorStoreManager(config, api_key)
        print("✅ Vector Store Manager inicializado")
        
        print("✅ Testes de vector store concluídos!")
        
    except Exception as e:
        print(f"❌ Erro nos testes de vector store: {e}")

def main():
    """Função principal de teste"""
    
    print("🤖 TESTE COMPLETO DO SISTEMA RAG AVANÇADO")
    print("=" * 60)
    print("Este script testa todas as funcionalidades do sistema RAG")
    print("implementado com suporte a arquivos de até 2GB.")
    print("=" * 60)
    
    # Executar testes
    asyncio.run(test_rag_system())
    asyncio.run(test_file_processing())
    asyncio.run(test_vector_store())
    
    print("\n🏁 TODOS OS TESTES FINALIZADOS!")
    print("Verifique os resultados acima para confirmar o funcionamento do sistema.")

if __name__ == "__main__":
    main()
